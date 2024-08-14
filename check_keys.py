import asyncio
import datetime
import logging

from config import INTERVAL, bot
from database.controllers.key import delete_key
from database.controllers.order import get_all_orders, delete_order
from keyboards.profile import get_order_expiring_keyboard
from schemas import OrderModel
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


async def check_expired():
    now = datetime.datetime.now(datetime.timezone.utc)
    logging.log(level=logging.INFO, msg=str(now))
    orders = get_all_orders()
    for order in orders:
        expire = order.expiration_date.astimezone(datetime.timezone.utc)
        hour_before = now + datetime.timedelta(hours=1, minutes=0)
        fift_mins_before = now + datetime.timedelta(hours=0, minutes=15)
        five_mins_before = now + datetime.timedelta(hours=0, minutes=5)
        day_before = now + datetime.timedelta(days=1)
        interval = datetime.timedelta(minutes=INTERVAL, seconds=10)
        logging.log(level=logging.INFO, msg=str(hour_before - interval))
        logging.log(level=logging.INFO, msg=str(expire))
        logging.log(level=logging.INFO, msg=str(hour_before))
        if expire <= now:
            await order_expired(order)
        elif five_mins_before - interval < expire <= five_mins_before:
            await order_going_to_expired(order, str((expire - now).seconds // 60) + " минут")
        elif fift_mins_before - interval < expire <= fift_mins_before:
            await order_going_to_expired(order, str((expire - now).seconds // 60) + " минут")
        elif hour_before - interval < expire <= hour_before:
            await order_going_to_expired(order, "1 час")
        elif day_before - interval < expire <= day_before:
            await order_going_to_expired(order, "1 день")


async def main():
    while True:
        await check_expired()
        await asyncio.sleep(INTERVAL * 60)


if __name__ == "__main__":
    asyncio.run(main())
