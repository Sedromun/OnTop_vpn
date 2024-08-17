from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CONNECT_INSTR_URL
from database.controllers.user import get_user_orders, register_user, get_user
from text.keyboard_text import *


def get_profile_keyboard(id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=top_up_balance,
        callback_data=ProfileCallbackFactory(balance=True, order_id=-1),
    )
    user = get_user(id)
    if user is None:
        register_user(id)
    orders = get_user_orders(id)
    for order in orders:
        builder.button(
            text=get_order_short_text(order.id, order.country),
            callback_data=ProfileCallbackFactory(balance=False, order_id=order.id),
        )
    builder.adjust(1)
    return builder.as_markup()


class ProfileCallbackFactory(CallbackData, prefix="profile"):
    balance: bool
    order_id: int


def get_order_changes_keyboard(id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=change_country,
        callback_data=OrderChangesCallbackFactory(text=change_country, id=id),
    )
    builder.button(
        text=extend_key,
        callback_data=OrderChangesCallbackFactory(text=extend_key, id=id),
    )
    builder.button(text=connect_instr, url=CONNECT_INSTR_URL)
    builder.button(
        text=back, callback_data=OrderChangesCallbackFactory(text=back, id=id)
    )
    builder.adjust(1)
    return builder.as_markup()


class OrderChangesCallbackFactory(CallbackData, prefix="order_changes"):
    text: str
    id: int


def get_order_countries_keyboard(id: int):
    builder = InlineKeyboardBuilder()
    for name, flag in COUNTRIES.items():
        builder.button(
            text=get_country_text(name, flag),
            callback_data=ChooseCountryChangeCallbackFactory(id=id, country=name),
        )
    builder.button(
        text=back,
        callback_data=ChooseCountryChangeCallbackFactory(id=id, country="", back=True),
    )
    builder.adjust(1)
    return builder.as_markup()


class ChooseCountryChangeCallbackFactory(CallbackData, prefix="country_change"):
    id: int
    country: str
    back: bool = False


def get_add_money_keyboard():
    builder = InlineKeyboardBuilder()

    adds = [100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000]
    for amount in adds:
        builder.button(
            text=str(amount),
            callback_data=ProfileAddMoneyCallbackFactory(amount=amount, duration=0),
        )
    builder.button(
        text=back,
        callback_data=ProfileAddMoneyCallbackFactory(amount=0, duration=0, back=True),
    )
    builder.adjust(3, 3, 3, 1)
    return builder.as_markup()


class ProfileAddMoneyCallbackFactory(CallbackData, prefix="profile_add_money"):
    amount: int
    duration: int
    back: bool = False


def get_order_expiring_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=extend_key,
        callback_data=OrderExpiringCallbackFactory(id=order_id),
    )
    builder.adjust(3, 3, 3, 1)
    return builder.as_markup()


class OrderExpiringCallbackFactory(CallbackData, prefix="profile_order_expiring"):
    id: int
