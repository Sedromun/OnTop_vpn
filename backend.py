import datetime

import uvicorn
from starlette.responses import HTMLResponse

from config import FERNET, HOST, PERCENT_REFERRAL, PORT, bot
from database.controllers.action import create_action
from database.controllers.order import create_order, get_order, update_order
from database.controllers.user import get_user, update_user
from keyboards.info import get_instruction_button_keyboard
from keyboards.profile import get_order_expiring_keyboard
from logs import backend_logger
from main import app
from schemas.Notification import NotificationSchema
from servers.outline_keys import get_key
from servers.vless_keys import get_vless_keys
from text.notifications import (auto_extended_failure, auto_extended_success,
                                get_referral_bought)
from text.profile import (get_money_added_text, get_order_info_text,
                          get_success_extended_key_text)
from text.texts import get_success_created_key_text
from utils.payment import get_order_perm_key
from utils.payment_handle import PaymentPurpose


async def check_referral(user_id, amount):
    user = get_user(user_id)
    if user is not None and user.referrer_id is not None:
        referrer = get_user(user.referrer_id)
        add_amount = amount * PERCENT_REFERRAL // 100 + 1
        update_user(user.referrer_id, {"balance": referrer.balance + add_amount})
        await bot.send_message(referrer.id, text=get_referral_bought(add_amount))


@app.post("/yoomoney/order_info")
async def check_payment(notification: NotificationSchema):
    backend_logger.info("POST - /yoomoney/order_info - new notification")
    payment = notification.object
    data = payment["metadata"]

    if "extending" in data:
        order = get_order(data["order_id"])
        if payment["status"] == "succeeded":
            update_order(
                order.id,
                {
                    "expiration_date": order.expiration_date.astimezone(
                        datetime.timezone.utc
                    )
                    + datetime.timedelta(days=31),
                },
            )
            create_action(
                user_id=order.user_id,
                title="extend key",
                description="auto - success"
            )
            await bot.send_message(order.user_id, text=auto_extended_success(order.id))
        else:
            update_order(
                order.id,
                {
                    "expiration_date": order.expiration_date.astimezone(
                        datetime.timezone.utc
                    )
                    + datetime.timedelta(days=1),
                    "payment_id": "",
                },
            )
            create_action(
                user_id=order.user_id,
                title="extend key",
                description="auto - FAILED"
            )

            await bot.send_message(
                order.user_id,
                text=auto_extended_failure(order.id),
                reply_markup=get_order_expiring_keyboard(order.id),
            )
        return

    if payment["status"] == "succeeded":
        duration_str = data["duration"]
        order_id = int(data["order_id"])
        purpose = int(data["purpose"])
        user_id = int(data["user_id"])
        order = get_order(order_id)
        amount = int(float(payment["amount"]["value"]))
        title = ""
        description = f"card, amount: {amount}"

        if (
                purpose == PaymentPurpose.BUY_CARD.value
                or purpose == PaymentPurpose.BUY_ADD_MONEY.value
        ):
            title = "buy key"
            begin = datetime.datetime.now(datetime.timezone.utc)
            end = begin + datetime.timedelta(days=int(data["duration"]))
            order = create_order(
                {
                    "user_id": user_id,
                    "country": data["country"],
                    "begin_date": begin,
                    "expiration_date": end,
                    "price": int(data["price"]),
                    "payment_id": payment["payment_method"]["id"],
                }
            )

            description += f"county: {order.country}"

            get_key(order.country, order.id)

            await bot.send_message(
                user_id,
                text=get_success_created_key_text(get_order_perm_key(order.id))
                     + get_order_info_text(order.id),
                reply_markup=get_instruction_button_keyboard(),
            )

        user = get_user(user_id)
        if purpose == PaymentPurpose.ADD_MONEY.value:
            new_balance = user.balance + amount
            update_user(user_id, {"balance": new_balance})
            title = "add money to balance"
            description = str(amount)
            await bot.send_message(user_id, text=get_money_added_text())
        elif (
                purpose == PaymentPurpose.EXTEND_ADD_MONEY.value
                or purpose == PaymentPurpose.BUY_ADD_MONEY.value
        ):
            price = int(data["price"])
            update_order(order.id, {"price": price})
            new_balance = user.balance + amount - price
            description = f"add money, price: {price}, amount: {amount}"
            update_user(user.id, {"balance": new_balance})

        if (
                purpose == PaymentPurpose.EXTEND_ADD_MONEY.value
                or purpose == PaymentPurpose.EXTEND_CARD.value
        ):
            title = "extend key"
            begin = order.expiration_date
            end = begin + datetime.timedelta(days=int(duration_str))
            update_order(
                order.id,
                {"expiration_date": end, "payment_id": payment["payment_method"]["id"]},
            )

            description += f"county: {order.country}"

            await bot.send_message(
                user_id,
                text=get_success_extended_key_text() + get_order_info_text(order.id),
            )

        try:
            await bot.delete_message(user_id, data["message_id"])
        except Exception:
            pass

        create_action(
            user_id=user_id,
            title=title,
            description=description
        )

        await check_referral(user_id, amount)


@app.get("/keys/{order_id_enc}")
async def get_key_id(order_id_enc: str):
    order_id = FERNET.decrypt(order_id_enc.encode()).decode()
    order = get_order(int(order_id))
    key = get_key(order.country, order_id)
    return HTMLResponse(key)

@app.get("/vless/{order_id_enc}")
async def get_vless_perm_keys(order_id_enc: str):
    order_id = FERNET.decrypt(order_id_enc.encode()).decode()
    expiry_time, key = await get_vless_keys(order_id)
    return HTMLResponse(key, headers={"Profile-Title": "Clique VPN", "Subscription-Userinfo": f'upload=17477; download=113814; total=0; expire={str(expiry_time)}'})

@app.get("/")
async def root():
    return "Hello!"


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
