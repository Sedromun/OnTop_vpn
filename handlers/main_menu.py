from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from config import WELCOME_PRESENT
from database.controllers.user import get_user, register_user, update_user
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
    user_id = message.from_user.id
    user = get_user(user_id)
    referrer = None
    if user is None:

        if " " in message.text:
            referrer_candidate = message.text.split()[1]

            try:
                referrer_candidate = int(referrer_candidate)
                ref_can = get_user(referrer_candidate)
                if ref_can is not None and user_id != referrer_candidate:
                    referrer = ref_can
            except ValueError:
                pass
        _ = register_user(message.from_user.id)

    if referrer is not None:
        update_user(user_id, {'balance': WELCOME_PRESENT, 'referrer_id': referrer.id})

    await message.answer(
        text=get_greeting_text(),
        reply_markup=get_main_keyboard()
    )


@main_router.message(StateFilter(None), F.text == buy)
async def buy_handler(message: Message):
    user = get_user(message.from_user.id)
    if user is None:
        register_user(message.from_user.id)
    await message.answer(
        text=get_buy_vpn_text(), reply_markup=get_buy_vpn_keyboard(user_id=message.from_user.id, extend=False)
    )


@main_router.message(StateFilter(None), F.text == info)
async def info_handler(message: Message):
    await message.answer(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )


@main_router.message(StateFilter(None), F.text == profile)
async def profile_handler(message: Message):
    id = message.from_user.id
    user = get_user(id)
    if user is None:
        register_user(id)
    await message.answer(
        text=get_profile_text(id), reply_markup=get_profile_keyboard(id)
    )


@main_router.message(StateFilter(None))
async def incorrect_command_handler(message: Message):
    await message.answer(get_incorrect_command())
