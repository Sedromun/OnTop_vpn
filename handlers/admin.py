import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINS, bot
from database.controllers.order import get_all_orders
from database.controllers.user import get_all_users, update_user, get_user
from states import AdminBaseStates, MainBaseState
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


@admin_router.message(Command("send_message_to_all_users"))
async def choose_country_callback(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.set_state(AdminBaseStates.send_to_all)
    await message.answer("Введите сообщение которое нужно разослать ВСЕМ пользователям\n"
                         "/cancel - для отмены")


@admin_router.message(AdminBaseStates.send_to_all, Command("cancel"))
async def choose_country_callback(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.clear()
    await message.answer("Отменено")


@admin_router.message(AdminBaseStates.send_to_all)
async def choose_country_callback(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.set_state(AdminBaseStates.confirm)
    await state.set_data({'message_id': message.message_id})
    await message.answer("Подтвердите, что все верно - для этого необходимо написать 'confirm - подтверждаю'")


@admin_router.message(AdminBaseStates.confirm, F.text == "confirm - подтверждаю")
async def choose_country_callback(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    message_id = (await state.get_data())['message_id']

    users = get_all_users()
    for user in users:
        await bot.copy_message(user.id, message.chat.id, message_id)

    await state.clear()
    await message.answer("сообщение разослано")


@admin_router.message(AdminBaseStates.confirm)
async def choose_country_callback(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.clear()
    await message.answer("отменено")
