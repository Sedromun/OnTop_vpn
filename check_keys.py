import asyncio
import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from yookassa import Payment

from config import INTERVAL, bot, ONE_DAY_SALE
from database.controllers.key import delete_key
from database.controllers.order import get_all_orders, delete_order
from database.controllers.user import get_all_users, update_user
from keyboards.profile import get_order_expiring_keyboard
from schemas import OrderModel
from text.notifications import new_user_notification_text, sale_one_day_notification_text
from text.texts import order_expired_text, order_going_to_expired_text
from utils.buy_options import Prices


async def order_expired(order: OrderModel):
    payment_id = order.payment_id
    if payment_id is not None and payment_id != "":
        payment = Payment.create({
            "amount": {
                "value": Prices['1 месяц'],
                "currency": "RUB"
            },
            "capture": True,
            "payment_method_id": payment_id,
            "description": f"Продление Clique VPN, ключ №{order.id} на месяц",
            "metadata": {
                "extending": True,
                "order_id": order.id
            }
        })
    else:
        for key in order.keys:
            delete_key(key.id)
        order_id = order.id
        user_id = order.user_id
        delete_order(order.id)
        await bot.send_message(user_id, order_expired_text(order_id))


async def order_going_to_expired(order: OrderModel, time: str):
    if order.payment_id is None or order.payment_id == "":
        await bot.send_message(
            order.user_id,
            order_going_to_expired_text(order.id, time),
            reply_markup=get_order_expiring_keyboard(order.id)
        )


async def new_user_notification(user, _: str):
    await bot.send_message(
        user.id,
        new_user_notification_text()
    )


async def sale_one_day_notification(user, _: str):
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


async def check_on_time(func, now, target_time, interval, after: bool, model, interval_name):
    checks_interval = datetime.timedelta(minutes=INTERVAL, seconds=0)
    tm = target_time + interval * (1 if after else -1)
    if now - checks_interval < tm < now:
        await func(model, interval_name)


ORDERS_NOTIFICATIONS = [
    (order_going_to_expired, datetime.timedelta(hours=1, minutes=0), False, "1 час"),
    (order_going_to_expired, datetime.timedelta(days=1, minutes=0), False, "1 день"),
    (order_expired, datetime.timedelta(minutes=0), False, "сейчас")
]

USERS_NOTIFICATIONS = [
    (new_user_notification, datetime.timedelta(hours=0, minutes=20), True),
    (sale_one_day_notification, datetime.timedelta(days=1), True)
]


async def check_expired():
    now = datetime.datetime.now(datetime.timezone.utc)
    orders = get_all_orders()
    for order in orders:
        if not order.keys:
            continue
        expire = order.expiration_date.astimezone(datetime.timezone.utc)
        for (func, interval, after, interval_name) in ORDERS_NOTIFICATIONS:
            await check_on_time(
                func,
                now,
                expire,
                interval,
                after,
                order,
                interval_name
            )

    users = get_all_users()
    for user in users:
        if not user.orders:
            for (func, interval, after) in USERS_NOTIFICATIONS:
                await check_on_time(
                    func,
                    now,
                    user.created_time.astimezone(datetime.timezone.utc),
                    interval,
                    after,
                    user,
                    ""
                )


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_expired, trigger=IntervalTrigger(minutes=INTERVAL))
    scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())
