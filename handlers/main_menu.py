from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from database.controllers.user import get_user, register_user
from keyboards.buy import get_buy_vpn_keyboard
from keyboards.info import get_info_keyboard
from keyboards.main_keyboard import get_main_keyboard
from keyboards.profile import get_profile_keyboard
from text.keyboard_text import buy, info, profile
from text.texts import (
    get_buy_vpn_text,
    get_greeting_text,
    get_incorrect_command,
    get_information_text,
    get_profile_text,
)

main_router = Router(name="main")


@main_router.message(StateFilter(None), Command("start"))
async def start_handler(message: Message):
    user = get_user(message.from_user.id)
    if user is None:
        _ = register_user(message.from_user.id)

    await message.answer(get_greeting_text(), reply_markup=get_main_keyboard())


@main_router.message(StateFilter(None), F.text == buy)
async def buy_handler(message: Message):
    await message.answer(
        text=get_buy_vpn_text(), reply_markup=get_buy_vpn_keyboard(extend=False)
    )


@main_router.message(StateFilter(None), F.text == info)
async def info_handler(message: Message):
    await message.answer(text=get_information_text(), reply_markup=get_info_keyboard())


@main_router.message(StateFilter(None), F.text == profile)
async def profile_handler(message: Message):
    id = message.from_user.id
    await message.answer(
        text=get_profile_text(id), reply_markup=get_profile_keyboard(id)
    )


@main_router.message(StateFilter(None))
async def incorrect_command_handler(message: Message):
    await message.answer(get_incorrect_command())
