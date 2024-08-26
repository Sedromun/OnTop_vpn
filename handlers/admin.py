import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMINS
from database.controllers.order import get_all_orders
from database.controllers.user import get_all_users, update_user, get_user
from text.texts import get_incorrect_command

admin_router = Router(name="admin")


@admin_router.message(Command("starts_stat"))
async def choose_country_callback(message: Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    users = get_all_users()
    last_days_users_cnt = 0
    for user in users:
        if (datetime.datetime.now(datetime.timezone.utc) - user.created_time).days == 0:
            last_days_users_cnt += 1
    await message.answer("Всего запусков: " + str(len(users)) + "\n" +
                         "Запусков за последние сутки: " + str(last_days_users_cnt) + "\n")


@admin_router.message(Command("buys_stat"))
async def choose_country_callback(message: Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    orders = get_all_orders()

    last_days_orders_cnt = 0
    orders_cnt = 0
    for order in orders:
        if order.keys:
            orders_cnt += 1
            if (datetime.datetime.now(datetime.timezone.utc) - order.created_time).days == 0:
                last_days_orders_cnt += 1

    await message.answer("Всего покупок: " + str(orders_cnt) + "\n" +
                         "Покупок за последние сутки: " + str(last_days_orders_cnt) + "\n")


@admin_router.message(Command("give_money"))
async def choose_country_callback(message: Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return
    try:
        _, user_id_str, money_str = message.text.split(' ')
    except ValueError:
        await message.answer("Неверно введена команда")
        return

    if user_id_str is None or money_str is None:
        await message.answer("Неверно введена команда")
        return
    try:
        user_id = int(user_id_str)
        money = int(money_str)
    except ValueError:
        await message.answer("Неверная команда")
        return

    user = get_user(user_id)
    if user is None:
        await message.answer("Такого юзера нет")

    update_user(user_id, {'balance': user.balance + money})
