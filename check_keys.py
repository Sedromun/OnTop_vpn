import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from yookassa import Configuration, Payment

from config import INTERVAL, ONE_DAY_SALE, SECRET_KEY, SHOP_ID, bot, THIRD_DAY_SALE
from database.controllers.key import delete_key
from database.controllers.order import delete_order, get_all_orders, create_order
from database.controllers.user import get_all_users, update_user
from keyboards.profile import get_order_expiring_keyboard, sale_week_notification_keyboard
from logs import logging, checker_logger
from schemas import OrderModel, FinishedOrderModel
from text.notifications import (new_user_notification_text,
                                sale_one_day_notification_text, order_expired_text, order_going_to_expired_text,
                                sale_three_day_notification_text, sale_week_notification_text)
from utils.buy_options import OLD_PRICES


async def order_expired(order: OrderModel, _: str):
    payment_id = order.payment_id
    if payment_id is not None and payment_id != "":
        logging.info(f"created autopayment order {order.id}")
        payment = Payment.create(
            {
                "amount": {"value": OLD_PRICES["1 месяц"], "currency": "RUB"},
                "capture": True,
                "payment_method_id": payment_id,
                "description": f"Продление Clique VPN, ключ №{order.id} на месяц",
                "metadata": {"extending": True, "order_id": order.id},
            }
        )
    else:
        logging.info(f"order {order.id} - expired")
        for key in order.keys:
            delete_key(key.id)
        order_id = order.id
        user_id = order.user_id
        country = order.country
        create_order(order._asdict(), FinishedOrderModel)
        delete_order(order.id)
        await bot.send_message(user_id, order_expired_text(order_id, country))


async def order_going_to_expired(order: OrderModel, time: str):
    logging.info(f"soon order {order.id} will be expired, sent notification")
    if order.payment_id is None or order.payment_id == "":
        await bot.send_message(
            order.user_id,
            order_going_to_expired_text(order.id, order.country, time),
            reply_markup=get_order_expiring_keyboard(order.id),
        )


async def new_user_notification(user, _: str):
    logging.info(f"new user {user.id} notification")
    await bot.send_message(user.id, new_user_notification_text())


async def sale_one_day_notification(user, _: str):
    logging.info(f"user {user.id} got sale notification")
    await bot.send_message(user.id, sale_one_day_notification_text())
    if user.sale is None or user.sale <= ONE_DAY_SALE:
        update_user(
            user.id,
            {
                "sale": ONE_DAY_SALE,
                "sale_expiration": datetime.datetime.now(datetime.timezone.utc)
                                   + datetime.timedelta(days=1),
            },
        )


async def first_order_finished_notification(order, _: str):
    user = order.user
    logging.info(f"user {user.id} got sale notification 20% at 3 days after expiration")

    await bot.send_message(user.id, sale_three_day_notification_text(order.id))
    if user.sale is None or user.sale <= THIRD_DAY_SALE:
        update_user(
            user.id,
            {
                "sale": THIRD_DAY_SALE,
                "sale_expiration": datetime.datetime.now(datetime.timezone.utc)
                                   + datetime.timedelta(days=1),
            },
        )


async def second_order_finished_notification(order, _: str):
    user = order.user
    logging.info(f"user {user.id} got week notification why bad vpn")

    await bot.send_message(
        user.id,
        sale_week_notification_text(),
        reply_markup=sale_week_notification_keyboard(order.id)
    )


async def check_on_time(
        func, now, target_time, interval, after: bool, model, interval_name
):
    checks_interval = datetime.timedelta(minutes=INTERVAL, seconds=0)
    tm = target_time + interval * (1 if after else -1)
    if now - checks_interval < tm < now:
        await func(model, interval_name)


ORDERS_NOTIFICATIONS = [
    (order_going_to_expired, datetime.timedelta(hours=1, minutes=0), False, "1 час"),
    (order_going_to_expired, datetime.timedelta(days=1, minutes=0), False, "1 день"),
    (order_expired, datetime.timedelta(minutes=0), False, "сейчас"),
]

USERS_NOTIFICATIONS = [
    (new_user_notification, datetime.timedelta(hours=0, minutes=15), True),
    (sale_one_day_notification, datetime.timedelta(days=1), True),
]

FINISHED_ORDERS_NOTIFICATIONS = [
    (first_order_finished_notification, datetime.timedelta(days=3), True),
    (second_order_finished_notification, datetime.timedelta(days=7), True),
]


async def check_expired():
    print("START")
    now = datetime.datetime.now(datetime.timezone.utc)
    orders = get_all_orders()
    for order in orders:
        if not order.keys:
            continue
        expire = order.expiration_date.astimezone(datetime.timezone.utc)
        for func, interval, after, interval_name in ORDERS_NOTIFICATIONS:
            await check_on_time(
                func, now, expire, interval, after, order, interval_name
            )

    users = get_all_users()
    for user in users:
        if not user.orders:
            for func, interval, after in USERS_NOTIFICATIONS:
                await check_on_time(
                    func,
                    now,
                    user.created_time.astimezone(datetime.timezone.utc),
                    interval,
                    after,
                    user,
                    "",
                )

    finished_orders = get_all_orders(model=FinishedOrderModel)
    checker_logger.info(msg=str(finished_orders))
    print(finished_orders)
    for order in finished_orders:
        print(order)
        user = order.user
        if not user.orders:
            expire = order.expiration_date.astimezone(datetime.timezone.utc)
            for func, interval, after in ORDERS_NOTIFICATIONS:
                await check_on_time(
                    func, now, expire, interval, after, order, ""
                )


if __name__ == "__main__":
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = SECRET_KEY

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_expired, "interval", seconds=60 * INTERVAL)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
