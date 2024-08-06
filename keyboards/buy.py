from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MIN_ADD_AMOUNT
from text.keyboard_text import balance, card, get_buy_option_text, get_country_text
from utils.buy_options import BuyOptions, get_option_duration, get_option_price
from utils.country import COUNTRIES


def get_buy_vpn_keyboard(extend: bool, order_id: int = -1):
    builder = InlineKeyboardBuilder()
    for option in BuyOptions:
        builder.button(
            text=get_buy_option_text(option),
            callback_data=BuyCallbackFactory(duration=get_option_duration(option),
                                             price=get_option_price(option),
                                             extend=extend,
                                             order_id=order_id).pack()
        )
    builder.adjust(1)
    return builder.as_markup()


class BuyCallbackFactory(CallbackData, prefix="buy_cho_opt"):
    duration: int  # in days
    price: int
    extend: bool
    order_id: int


def get_payment_countries_keyboard(duration: int, price: int):
    builder = InlineKeyboardBuilder()
    for name, flag in COUNTRIES.items():
        builder.button(
            text=get_country_text(name, flag),
            callback_data=ChooseCountryCallbackFactory(option=Payment.Balance.value, duration=duration, price=price,
                                                       country=name)
        )
    builder.adjust(1)
    return builder.as_markup()


class ChooseCountryCallbackFactory(CallbackData, prefix="country"):
    option: str
    duration: int
    price: int
    country: str


def get_payment_options_keyboard(duration: int, price: int, country: str, extend: bool, order_id: int = -1):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=balance,
        callback_data=PaymentCallbackFactory(option=Payment.Balance.value, duration=duration, price=price,
                                             country=country, extend=extend, order_id=order_id)
    )
    builder.button(
        text=card,
        callback_data=PaymentCallbackFactory(option=Payment.Card.value, duration=duration, price=price, country=country, extend=extend, order_id=order_id)
    )
    builder.adjust(1)
    return builder.as_markup()


class Payment(Enum):
    Balance = "Balance"
    Card = "Card"


class PaymentCallbackFactory(CallbackData, prefix="pay"):
    option: str
    duration: int
    price: int
    country: str
    extend: bool
    order_id: int


def get_balance_add_money_keyboard(duration: int, price: int, country: str, add: int, order_id: int = -1):
    builder = InlineKeyboardBuilder()

    if add >= MIN_ADD_AMOUNT:
        builder.button(
            text=str(add),
            callback_data=PaymentAddMoneyCallbackFactory(duration=duration, price=price, country=country, amount=add, order_id=order_id)
        )
    else:
        builder.button(
            text=str(MIN_ADD_AMOUNT),
            callback_data=PaymentAddMoneyCallbackFactory(duration=duration, price=price, country=country, amount=MIN_ADD_AMOUNT, order_id=order_id)
        )

    adds = [100, 200, 300, 500, 1000, 2000]
    for amount in adds:
        if amount >= add:
            builder.button(
                text=str(amount),
                callback_data=PaymentAddMoneyCallbackFactory(duration=duration, price=price, country=country, amount=amount, order_id=order_id)
            )
    builder.adjust(1, 3, 3)
    return builder.as_markup()


class PaymentAddMoneyCallbackFactory(CallbackData, prefix="pay_add_money"):
    duration: int
    price: int
    amount: int
    country: str
    order_id: int

