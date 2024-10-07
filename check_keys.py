import asyncio
import datetime
import logging

from config import INTERVAL, bot, ONE_DAY_SALE
from database.controllers.key import delete_key
from database.controllers.order import get_all_orders, delete_order
from database.controllers.user import get_all_users, update_user
from keyboards.profile import get_order_expiring_keyboard
from schemas import OrderModel
from text.notifications import new_user_notification_text, sale_one_day_notification_text
from text.texts import order_expired_text, order_going_to_expired_text


async def order_expired(order: OrderModel):
    for key in order.keys:
        delete_key(key.id)
    order_id = order.id
    user_id = order.user_id
    delete_order(order.id)
    await bot.send_message(user_id, order_expired_text(order_id))


async def order_going_to_expired(order: OrderModel, time: str):
    await bot.send_message(
        order.user_id,
        order_going_to_expired_text(order.id, time),
        reply_markup=get_order_expiring_keyboard(order.id)
    )


async def new_user_notification(user):
    await bot.send_message(
        user.id,
        new_user_notification_text()
    )


async def sale_one_day_notification(user):
    await bot.send_message(
        user.id,
        sale_one_day_notification_text()
    )
    if user.sale is None or user.sale <= ONE_DAY_SALE:
        update_user(user.id, {
            "sale": ONE_DAY_SALE,
            "sale_expiration":
                datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        })


async def check_expired():
    now = datetime.datetime.now(datetime.timezone.utc)
    orders = get_all_orders()
    for order in orders:
        if not order.keys:
            continue
        expire = order.expiration_date.astimezone(datetime.timezone.utc)
        hour_before = now + datetime.timedelta(hours=1, minutes=0)
        five_mins_before = now + datetime.timedelta(hours=0, minutes=5)
        day_before = now + datetime.timedelta(days=1)
        interval = datetime.timedelta(minutes=INTERVAL, seconds=10)
        if expire <= now:
            await order_expired(order)
        elif five_mins_before - interval < expire <= five_mins_before:
            await order_going_to_expired(order, "5 минут")
        elif hour_before - interval < expire <= hour_before:
            await order_going_to_expired(order, "1 час")
        elif day_before - interval < expire <= day_before:
            await order_going_to_expired(order, "1 день")

    users = get_all_users()
    for user in users:
        if not user.orders:
            twenty_mins_before = now - datetime.timedelta(hours=0, minutes=20)
            day_before = now - datetime.timedelta(days=1)
            interval = datetime.timedelta(minutes=INTERVAL, seconds=10)
            if twenty_mins_before - interval < user.created_time.astimezone(datetime.timezone.utc) <= twenty_mins_before:
                await new_user_notification(user)
            elif day_before - interval < user.created_time <= day_before:
                await sale_one_day_notification(user)



async def main():
    while True:
        await check_expired()
        await asyncio.sleep(INTERVAL * 60)


if __name__ == "__main__":
    asyncio.run(main())
