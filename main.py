import asyncio
import datetime

from aiogram.types import message
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from yookassa import Payment, Configuration
from yookassa.domain.notification import WebhookNotification

from config import bot, dp, FERNET, PERCENT_REFERRAL, SHOP_ID, SECRET_KEY
from database.controllers.order import get_order, update_order
from database.controllers.user import get_user, register_user, update_user
from handlers import buy_router, info_router, main_router, profile_router
from handlers.admin import admin_router
from schemas.Payment import PaymentSchema
from servers.outline_keys import get_key
from text.profile import get_order_info_text, get_success_extended_key_text, get_money_added_text
from text.texts import get_referral_bought, get_success_created_key_text
from utils.payment import get_order_perm_key

dp.include_router(admin_router)
dp.include_router(buy_router)
dp.include_router(profile_router)
dp.include_router(info_router)
dp.include_router(main_router)

app = FastAPI()


@app.post("/yoomoney/order_info")
async def check_payment(payment: PaymentSchema):
    print(str(payment))
    if payment.status == "succeeded":
        duration_str = payment.metadata['duration']
        order_id = int(payment.metadata['order_id'])
        extend = payment.metadata['extend']
        order = get_order(order_id)
        user_id = order.user_id
        user = get_user(user_id)
        if user is None:
            register_user(user_id)

        amount = payment.amount.value // 100

        if user.referrer_id is not None:
            referrer = get_user(user.referrer_id)
            add_amount = (amount * PERCENT_REFERRAL // 100)
            update_user(user.referrer_id, {'balance': referrer.balance + add_amount})
            await bot.send_message(referrer.id, text=get_referral_bought(add_amount))

        if extend == "E" or extend == "C":
            order = get_order(int(order_id))
            price = order.price
            new_balance = user.balance + amount - price
            update_user(user.id, {"balance": new_balance})
            if extend == "C":
                get_key(order.country, order.id)
                await bot.send_message(user_id,
                    text=get_success_created_key_text(get_order_perm_key(order.id)) + get_order_info_text(order.id)
                )
            else:
                begin = order.expiration_date
                end = begin + datetime.timedelta(days=int(duration_str))
                update_order(order.id, {"expiration_date": end})

                await bot.send_message(user_id,text=get_success_extended_key_text() + get_order_info_text(order.id))
        else:
            new_balance = user.balance + amount
            update_user(user_id, {"balance": new_balance})
            await bot.send_message(user_id, text=get_money_added_text())


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
