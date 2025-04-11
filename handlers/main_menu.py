import datetime

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject

from config import SECRET_START_STRING, SPECIAL_URLS, WELCOME_PRESENT
from database.controllers.action import create_action
from database.controllers.order import create_order, update_order
from database.controllers.present import get_present, update_present
from database.controllers.user import get_user, register_user, update_user
from keyboards.buy import get_buy_vpn_keyboard
from keyboards.info import get_info_keyboard
from keyboards.main_keyboard import get_main_keyboard
from logs import bot_logger
from text.info import get_referral_program_text
from servers.outline_keys import get_key

from text.keyboard_text import buy, referral_program, settings
from text.texts import (get_buy_vpn_text, get_greeting_text,
                        get_incorrect_command, get_information_text,
                        get_old_user_message_start_text, get_present_greeting_text)


main_router = Router(name="main")


@main_router.message(StateFilter(None), CommandStart(deep_link=True))
async def start_handler(message: Message, command: CommandObject):
    bot_logger.info(f"Message: '{message.message_id}' - main_menu.start_handler")

    user_id = message.from_user.id
    user = get_user(user_id)

    args = command.args

    if " " in message.text:
        try:
            payload = decode_payload(args)
            res = get_present(int(payload))
            if res is not None and res.activated == 0:
                if user is None:
                    user = register_user(message.from_user.id)
                begin = datetime.datetime.now(datetime.timezone.utc)
                end = begin + datetime.timedelta(days=res.duration)
                order = create_order(
                    {
                        "user_id": user.id,
                        "country": res.country,
                        "begin_date": begin,
                        "expiration_date": end,
                        "price": res.price,
                    }
                )
                get_key(order.country, order.id)
                update_present(res.id, {"activated": 1})
                await message.answer(text=get_present_greeting_text(), reply_markup=get_main_keyboard())
                return
        except:
            pass


    if user is not None:
        if " " in message.text:
            referrer_candidate = message.text.split()[1]
            if referrer_candidate == SECRET_START_STRING:
                await message.answer(
                    text=get_old_user_message_start_text(),
                    reply_markup=get_main_keyboard(),
                )
                create_action(
                    user_id=user.id,
                    title="start",
                    description="old user"
                )
                if user.present_for_old is None or user.present_for_old == False:
                    update_user(user.id, {"present_for_old": True})
                    orders = user.orders
                    for order in orders:
                        update_order(
                            order.id,
                            {
                                "expiration_date": order.expiration_date.astimezone(
                                    datetime.timezone.utc
                                )
                                + datetime.timedelta(days=14)
                            },
                        )
                return

    referrer = None
    if user is None:

        if " " in message.text:
            referrer_candidate = message.text.split()[1]
            for spec_url in SPECIAL_URLS.keys():
                if referrer_candidate == spec_url:
                    user = register_user(message.from_user.id)
                    update_user(user_id, {"balance": WELCOME_PRESENT})
                    create_action(
                        user_id=user.id,
                        title="start",
                        description=SPECIAL_URLS[spec_url]
                    )
                    return
            try:
                referrer_candidate = int(referrer_candidate)
                ref_can = get_user(referrer_candidate)
                if ref_can is not None and user_id != referrer_candidate:
                    referrer = ref_can
            except ValueError:
                pass
        user = register_user(message.from_user.id)


    if referrer is not None:
        update_user(user_id, {"balance": WELCOME_PRESENT, "referrer_id": referrer.id})
        create_action(
            user_id=user.id,
            title="start by referral",
            description=f"referrer: {referrer.id}"
        )
    else:
        create_action(
            user_id=user.id,
            title="start",
            description="new user"
        )

    await message.answer(text=get_greeting_text(), reply_markup=get_main_keyboard())


@main_router.message(StateFilter(None), Command("start"))
async def start_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - main_menu.start_handler")

    user_id = message.from_user.id
    user = get_user(user_id)

    if user is None:
        user = register_user(message.from_user.id)

    create_action(
        user_id=user.id,
        title="start",
        description="new user"
    )

    await message.answer(text=get_greeting_text(), reply_markup=get_main_keyboard())


@main_router.message(StateFilter(None), F.text == buy)
async def buy_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - main_menu.buy_handler")

    user = get_user(message.from_user.id)
    if user is None:
        register_user(message.from_user.id)
    await message.answer(
        text=get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(user_id=message.from_user.id, extend=False),
    )


@main_router.message(StateFilter(None), F.text == settings)
async def info_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - main_menu.info_handler")

    await message.answer(text=get_information_text(), reply_markup=get_info_keyboard())


@main_router.message(StateFilter(None), F.text == referral_program)
async def referral_handler(message: Message):
    bot_logger.info(f"Message: '{message.message_id}' - main_menu.referral_handler")

    await message.answer(text=get_referral_program_text(message.from_user.id))


@main_router.message(StateFilter(None))
async def incorrect_command_handler(message: Message):
    bot_logger.info(
        f"Message: '{message.message_id}' - main_menu.incorrect_command_handler"
    )

    await message.answer(get_incorrect_command())
