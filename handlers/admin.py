import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from config import ADMINS, bot, outline_client
from database.controllers.order import get_all_country_orders, get_all_orders
from database.controllers.user import get_all_users, get_user, update_user
from logs import bot_logger
from monitoring.monitoring import collect_user_info
from states import AdminBaseStates
from text.texts import get_incorrect_command
from utils.country import COUNTRIES

admin_router = Router(name="admin")


@admin_router.message(Command("starts_stat"))
async def admin_starts_stat_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_starts_stat_handler")
    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    users = get_all_users()
    last_days_users_cnt = 0
    for user in users:
        if (datetime.datetime.now(datetime.timezone.utc) - user.created_time).days == 0:
            last_days_users_cnt += 1
    await message.answer(
        "Всего запусков: "
        + str(len(users))
        + "\n"
        + "Запусков за последние сутки: "
        + str(last_days_users_cnt)
        + "\n"
    )


@admin_router.message(Command("buys_stat"))
async def admin_buys_stat_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_buys_stat_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    orders = get_all_orders()

    last_days_orders_cnt = 0
    orders_cnt = 0
    for order in orders:
        if order.keys:
            orders_cnt += 1
            if (
                datetime.datetime.now(datetime.timezone.utc) - order.created_time
            ).days == 0:
                last_days_orders_cnt += 1

    await message.answer(
        "Всего покупок: "
        + str(orders_cnt)
        + "\n"
        + "Покупок за последние сутки: "
        + str(last_days_orders_cnt)
        + "\n"
    )


@admin_router.message(Command("give_money"))
async def admin_give_money_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_give_money_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return
    try:
        _, user_id_str, money_str = message.text.split(" ")
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

    update_user(user_id, {"balance": user.balance + money})


@admin_router.message(Command("send_message_to_all_users"))
async def admin_send_message_handler(message: Message, state: FSMContext):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_send_message_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.set_state(AdminBaseStates.send_to_all)
    await message.answer(
        "Введите сообщение которое нужно разослать ВСЕМ пользователям\n"
        "/cancel - для отмены"
    )


@admin_router.message(AdminBaseStates.send_to_all, Command("cancel"))
async def admin_send_message_cancel_handler(message: Message, state: FSMContext):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_send_message_cancel_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.clear()
    await message.answer("Отменено")


@admin_router.message(AdminBaseStates.send_to_all)
async def admin_send_message_ask_confirm_handler(message: Message, state: FSMContext):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_send_message_ask_confirm_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.set_state(AdminBaseStates.confirm)
    await state.set_data({"message_id": message.message_id})
    await message.answer(
        "Подтвердите, что все верно - для этого необходимо написать 'confirm - подтверждаю'"
    )


@admin_router.message(AdminBaseStates.confirm, F.text == "confirm - подтверждаю")
async def admin_send_message_confirmed_handler(message: Message, state: FSMContext):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_send_message_confirmed_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    message_id = (await state.get_data())["message_id"]

    users = get_all_users()
    res = 0
    for user in users:
        try:
            await bot.copy_message(user.id, message.chat.id, message_id)
            res += 1
        except Exception:
            pass

    await state.clear()
    await message.answer("сообщение разослано, Всего: " + str(res))


@admin_router.message(AdminBaseStates.confirm)
async def admin_send_message_not_confirm_handler(message: Message, state: FSMContext):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_send_message_not_confirm_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await state.clear()
    await message.answer("отменено")


@admin_router.message(Command("countries_stat"))
async def admin_countries_stat_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_countries_stat_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    msg = ""

    for country in COUNTRIES.keys():
        orders = get_all_country_orders(country)
        msg += country + " : " + str(len(orders)) + "\n"

    await message.answer("Статистика по странам:\n\n" + msg)


@admin_router.message(Command("countries_server_stat"))
async def admin_countries_server_stat_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_countries_server_stat_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    msg = ""

    for country, client in outline_client.items():
        data = client.get_transferred_data()
        res = 0
        for byte in data["bytesTransferredByUserId"].values():
            res += byte
        msg += country + ": " + str(res / 10**9 * 100 // 10 / 10) + " Gb\n"

    await message.answer("Статистика по странам:\n\n" + msg)


@admin_router.message(Command("one_user_statistics"))
async def admin_one_user_statistics_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_one_user_statistics_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    try:
        _, user_id_str = message.text.split(" ")
        user_id = int(user_id_str)
    except ValueError:
        await message.answer("Неверно введена команда")
        return

    user = get_user(user_id)

    if not user:
        await message.answer("Такого юзера нет")

    user_stat = collect_user_info(user_id)

    await message.answer_document(BufferedInputFile(str(user_stat).encode('utf-8'), filename=f"user_{user_id}.json"))


@admin_router.message(Command("all_users_statistics"))
async def admin_all_users_statistics_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - admin.admin_all_users_statistics_handler")

    if str(message.from_user.id) not in ADMINS:
        await message.answer(get_incorrect_command())
        return

    await message.answer("это будет долго...")

    users = get_all_users()
    user_stat = []
    for user in users:
        user_stat.append(str(collect_user_info(user.id)))

    user_stat_str = "["

    for i in range(len(user_stat)):
        user_stat_str += user_stat[i] + (", " if i != len(user_stat) - 1 else "")
    user_stat_str += "]"

    await message.answer_document(BufferedInputFile(str(user_stat).encode('utf-8'), filename=f"users_stat.json"))
