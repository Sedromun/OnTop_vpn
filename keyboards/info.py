from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import RECALLS_TGC_TAG, RECALLS_TGC_LINK
from text.keyboard_text import *


def get_info_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=countries,
        callback_data=InfoCallbackFactory(text=countries)
    )
    builder.button(
        text=tech_support,
        callback_data=InfoCallbackFactory(text=tech_support)
    )
    builder.button(
        text=recalls,
        url=RECALLS_TGC_LINK
    )
    builder.adjust(1)
    return builder.as_markup()


class InfoCallbackFactory(CallbackData, prefix="info"):
    text: str


def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=back,
        callback_data=InfoBackCallbackFactory(back=True)
    )
    builder.adjust(1)
    return builder.as_markup()


class InfoBackCallbackFactory(CallbackData, prefix="info_back"):
    back: bool