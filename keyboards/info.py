from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import RECALLS_TGC_LINK, TECH_SUPPORT_LINK, INSTR_URL
from database.controllers.user import get_user, register_user, get_user_orders
from text.keyboard_text import *


def get_info_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=countries, callback_data=InfoCallbackFactory(text=countries))
    builder.button(text=referral_program, callback_data=InfoCallbackFactory(text=referral_program))
    builder.button(
        text=change_country,
        callback_data=InfoCallbackFactory(text=change_country),
    )
    builder.button(
        text=extend_key,
        callback_data=InfoCallbackFactory(text=extend_key),
    )
    builder.button(text=all_instr, url=INSTR_URL)
    builder.button(text=tech_support, url=TECH_SUPPORT_LINK)
    builder.button(text=recalls, url=RECALLS_TGC_LINK)
    builder.adjust(1)
    return builder.as_markup()


class InfoCallbackFactory(CallbackData, prefix="info"):
    text: str


def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=back, callback_data=InfoBackCallbackFactory(back=True))
    builder.adjust(1)
    return builder.as_markup()


class InfoBackCallbackFactory(CallbackData, prefix="info_back"):
    back: bool


def get_choose_order_keyboard(id: int, change_country: bool = False, extend_key: bool = False):
    builder = InlineKeyboardBuilder()

    user = get_user(id)
    if user is None:
        register_user(id)
    orders = get_user_orders(id)
    for order in orders:
        builder.button(
            text=get_order_short_text(order.id, order.country),
            callback_data=InfoChooseOrderCallbackFactory(
                change_country=change_country,
                extend_key=extend_key,
                order_id=order.id
            ),
        )

    builder.button(text=back, callback_data=InfoBackCallbackFactory(back=True))
    builder.adjust(1)
    return builder.as_markup()


class InfoChooseOrderCallbackFactory(CallbackData, prefix="info_cb"):
    change_country: bool = False
    extend_key: bool = False
    order_id: int


def get_instruction_button_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=all_instr, url=INSTR_URL)
    builder.adjust(1)
    return builder.as_markup()
