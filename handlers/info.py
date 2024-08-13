from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.info import (
    InfoBackCallbackFactory,
    InfoCallbackFactory,
    get_back_keyboard,
    get_info_keyboard,
)
from text.info import get_countries_text, get_referral_program_text
from text.keyboard_text import (
    countries,
    referral_program,
)
from text.texts import (
    get_information_text,
)

info_router = Router(name="info")


@info_router.callback_query(InfoCallbackFactory.filter(F.text == countries))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    await callback.message.edit_caption(
        caption=get_countries_text(), reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == referral_program))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    await callback.message.edit_caption(
        caption=get_referral_program_text(callback.from_user.id), reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoBackCallbackFactory.filter())
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoBackCallbackFactory
):
    await callback.message.edit_caption(
        caption=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()
