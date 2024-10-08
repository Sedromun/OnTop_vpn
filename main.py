import asyncio
import datetime

from aiogram.types import message
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from yookassa import Payment, Configuration
from yookassa.domain.notification import WebhookNotification

from config import bot, dp, FERNET, PERCENT_REFERRAL, SHOP_ID, SECRET_KEY
from database.controllers.order import get_order, update_order, create_order
from database.controllers.user import get_user, register_user, update_user
from handlers import buy_router, info_router, main_router, profile_router
from handlers.admin import admin_router
from keyboards.info import get_instruction_button_keyboard
from keyboards.profile import get_order_expiring_keyboard
from schemas.Notification import NotificationSchema
from schemas.Payment import PaymentSchema
from servers.outline_keys import get_key
from text.notifications import auto_extended_success, auto_extended_failure
from text.profile import get_order_info_text, get_success_extended_key_text, get_money_added_text
from text.texts import get_referral_bought, get_success_created_key_text
from utils.payment import get_order_perm_key
from utils.payment_handle import PaymentPurpose

dp.include_router(admin_router)
dp.include_router(buy_router)
dp.include_router(profile_router)
dp.include_router(info_router)
dp.include_router(main_router)

app = FastAPI()


async def check_referral(user_id, amount):
    user = get_user(user_id)
    if user is not None and user.referrer_id is not None:
        referrer = get_user(user.referrer_id)
        add_amount = (amount * PERCENT_REFERRAL // 100)
        update_user(user.referrer_id, {'balance': referrer.balance + add_amount})
        await bot.send_message(referrer.id, text=get_referral_bought(add_amount))


@app.post("/yoomoney/order_info")
async def check_payment(notification: NotificationSchema):
    payment = notification.object
    data = payment['metadata']

    if 'extending' in data:
        order = get_order(data['order_id'])
        if payment['status'] == 'succeeded':
            bot.send_message(order.user_id, text=auto_extended_success(order.id))
        else:
            update_order(order.id, {
                "expiration_date": order.expiration_date.astimezone(datetime.timezone.utc) + datetime.timedelta(days=1),
                "payment_id": ''
            })

            await bot.send_message(order.user_id,
                                   text=auto_extended_failure(order.id),
                                   reply_markup=get_order_expiring_keyboard(order.id))
        return

    if payment['status'] == "succeeded":
        duration_str = data['duration']
        order_id = int(data['order_id'])
        purpose = int(data['purpose'])
        user_id = int(data['user_id'])
        order = get_order(order_id)
        amount = (int(float(payment['amount']['value'])))

        if purpose == PaymentPurpose.BUY_CARD.value or purpose == PaymentPurpose.BUY_ADD_MONEY.value:
            begin = datetime.datetime.now(datetime.timezone.utc)
            end = begin + datetime.timedelta(days=int(data['duration']))
            order = create_order(
                {
                    "user_id": user_id,
                    "country": data['country'],
                    "begin_date": begin,
                    "expiration_date": end,
                    "price": int(data['price']),
                }
            )

            get_key(order.country, order.id)
            await bot.send_message(
                user_id,
                text=get_success_created_key_text(get_order_perm_key(order.id)) + get_order_info_text(order.id),
                reply_markup=get_instruction_button_keyboard()
            )

        user = get_user(user_id)
        if purpose == PaymentPurpose.ADD_MONEY.value:
            new_balance = user.balance + amount
            update_user(user_id, {"balance": new_balance})
            await bot.send_message(user_id, text=get_money_added_text())
        elif purpose == PaymentPurpose.EXTEND_ADD_MONEY.value or purpose == PaymentPurpose.BUY_ADD_MONEY.value:
            price = int(data['price'])
            update_order(order.id, {'price': price})
            new_balance = user.balance + amount - price
            update_user(user.id, {"balance": new_balance})

        if purpose == PaymentPurpose.EXTEND_ADD_MONEY.value or purpose == PaymentPurpose.EXTEND_CARD.value:
            begin = order.expiration_date
            end = begin + datetime.timedelta(days=int(duration_str))
            update_order(order.id, {"expiration_date": end})

            await bot.send_message(user_id, text=get_success_extended_key_text() + get_order_info_text(order.id))

        try:
            await bot.delete_message(user_id, data['message_id'])
        except Exception:
            pass

        await check_referral(user_id, amount)
        if purpose != PaymentPurpose.ADD_MONEY.value:
            update_order(order.id, {'payment_id': payment['payment_method']['id']})


@app.get("/keys/{order_id_enc}")
async def get_key_id(order_id_enc: str):
    order_id = FERNET.decrypt(order_id_enc.encode()).decode()
    order = get_order(int(order_id))
    key = get_key(order.country, order_id)
    return HTMLResponse(key)


@app.get("/")
async def root():
    return "Hello!"


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = SECRET_KEY
    asyncio.run(main())
