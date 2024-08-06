from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from text.keyboard_text import buy, profile, info


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text=buy))
    builder.add(types.KeyboardButton(text=profile))
    builder.add(types.KeyboardButton(text=info))
    builder.adjust(1, 2)

    return builder.as_markup(one_time_keyboard=False, resize_keyboard=True)
