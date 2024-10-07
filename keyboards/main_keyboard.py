from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from text.keyboard_text import buy, settings, profile, referral_program


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text=buy))
    builder.add(types.KeyboardButton(text=referral_program))
    builder.add(types.KeyboardButton(text=settings))
    builder.adjust(1, 2)

    return builder.as_markup(one_time_keyboard=False, resize_keyboard=True)
