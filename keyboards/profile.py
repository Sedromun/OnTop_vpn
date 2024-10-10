from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import INSTR_URL
from database.controllers.user import get_user, get_user_orders, register_user
from text.keyboard_text import *


def get_order_changes_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=all_instr, url=INSTR_URL)
    builder.button(text=settings, callback_data=BackKeyInfoCallbackFactory())
    builder.adjust(1)
    return builder.as_markup()


class BackKeyInfoCallbackFactory(CallbackData, prefix="order_changes"):
    pass


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


def sale_week_notification_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text=bad_price,
        callback_data=InfoVPNNotificationCallbackFactory(text=bad_price, order_id=order_id),
    )
    builder.button(
        text=bad_quality,
        callback_data=InfoVPNNotificationCallbackFactory(text=bad_quality, order_id=order_id),
    )
    builder.button(
        text=another_service,
        callback_data=InfoVPNNotificationCallbackFactory(text=another_service, order_id=order_id),
    )
    builder.button(
        text=dont_vpn,
        callback_data=InfoVPNNotificationCallbackFactory(text=dont_vpn, order_id=order_id),
    )
    builder.button(
        text=forgot_buy,
        callback_data=InfoVPNNotificationCallbackFactory(text=forgot_buy, order_id=order_id),
    )

    builder.adjust(1)
    return builder.as_markup()


class InfoVPNNotificationCallbackFactory(CallbackData, prefix="info_vpn"):
    text: str
    order_id: int


def get_buy_vpn_from_notify_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=buy,
        callback_data=BuyVPNFromNotificationCallbackFactory(),
    )

    builder.adjust(1)
    return builder.as_markup()


class BuyVPNFromNotificationCallbackFactory(CallbackData, prefix="buy_vpn_notify"):
    pass
