from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CONNECT_INSTR_URL, RECALLS_TGC_LINK, TECH_SUPPORT_LINK, BUY_INSTR_URL, CHANGE_COUNTRY_INSTR_URL
from text.keyboard_text import *


def get_info_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=countries, callback_data=InfoCallbackFactory(text=countries))
    builder.button(text=referral_program, callback_data=InfoCallbackFactory(text=referral_program))
    builder.button(text=connect_instr, url=CONNECT_INSTR_URL)
    builder.button(text=buy_instr, url=BUY_INSTR_URL)
    builder.button(text=change_country_instr, url=CHANGE_COUNTRY_INSTR_URL)
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
