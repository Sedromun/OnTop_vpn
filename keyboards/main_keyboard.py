from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import INSTR_URL
from text.keyboard_text import buy, referral_program, settings, all_instr


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text=buy))
    builder.add(types.KeyboardButton(text=referral_program))
    builder.add(types.KeyboardButton(text=settings))
    builder.adjust(1, 2)

    return builder.as_markup(one_time_keyboard=False, resize_keyboard=True)


def get_instr_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=all_instr,
        url=INSTR_URL
    )

    builder.adjust(1)
    return builder.as_markup()
