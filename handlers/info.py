import datetime

from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from aiogram import F, Router, types

from config import dp, bot, PAYMENTS_PROVIDER_TOKEN
from database.controllers.order import create_order, get_order, update_order
from database.controllers.user import get_user, update_user
from keyboards.info import InfoCallbackFactory, get_back_keyboard, InfoBackCallbackFactory, get_info_keyboard
from text.info import get_countries_text, get_tech_support_text, get_recalls_text
from utils.payment import buy_handle
from keyboards.buy import BuyCallbackFactory, get_payment_options_keyboard, PaymentCallbackFactory, Payment, \
    get_payment_countries_keyboard, get_buy_vpn_keyboard, get_balance_add_money_keyboard, \
    PaymentAddMoneyCallbackFactory, ChooseCountryCallbackFactory
from keyboards.profile import ProfileCallbackFactory, get_order_changes_keyboard, OrderChangesCallbackFactory, \
    get_order_countries_keyboard, get_profile_keyboard, ChooseCountryChangeCallbackFactory, get_add_money_keyboard, \
    ProfileAddMoneyCallbackFactory
from servers.outline_keys import get_key, key_change_country
from text.keyboard_text import buy, change_country, extend_key, back, countries, tech_support, recalls
from text.profile import get_order_info_text, get_order_choose_country_text, get_country_changed_text, \
    get_success_extended_key_text, get_profile_add_money_text
from text.texts import get_payment_option_text, get_success_created_key_text, get_payment_choose_country_text, \
    get_buy_vpn_text, get_not_enough_money_text, get_pay_text, get_profile_text, get_information_text

info_router = Router(name="info")


@info_router.callback_query(InfoCallbackFactory.filter(F.text == countries))
async def info_countries_callback(
        callback: CallbackQuery,
        callback_data: InfoCallbackFactory
):
    await callback.message.edit_text(
        text=get_countries_text(),
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == tech_support))
async def info_countries_callback(
        callback: CallbackQuery,
        callback_data: InfoCallbackFactory
):
    await callback.message.edit_text(
        text=get_tech_support_text(),
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == recalls))
async def info_countries_callback(
        callback: CallbackQuery,
        callback_data: InfoCallbackFactory
):
    await callback.message.edit_text(
        text=get_recalls_text(),
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoBackCallbackFactory.filter())
async def info_countries_callback(
        callback: CallbackQuery,
        callback_data: InfoBackCallbackFactory
):
    await callback.message.edit_text(text=get_information_text(), reply_markup=get_info_keyboard())
    await callback.answer()
