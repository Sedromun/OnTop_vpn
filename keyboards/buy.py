from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MIN_ADD_AMOUNT
from text.keyboard_text import (
    back,
    balance,
    card,
    get_buy_option_text,
    get_country_text,
)
from utils.buy_options import BuyOptions, get_option_duration, get_option_price
from utils.country import COUNTRIES


def get_buy_vpn_keyboard(extend: bool, order_id: int = -1, need_back: bool = False):
    builder = InlineKeyboardBuilder()
    for option in BuyOptions:
        builder.button(
            text=get_buy_option_text(option),
            callback_data=BuyCallbackFactory(
                duration=get_option_duration(option),
                price=get_option_price(option),
                extend=extend,
                order_id=order_id,
            ).pack(),
        )
    if need_back:
        builder.button(
            text=back,
            callback_data=BuyCallbackFactory(
                duration=get_option_duration(option),
                price=get_option_price(option),
                extend=extend,
                order_id=order_id,
                back=True,
            ).pack(),
        )
    builder.adjust(1)
    return builder.as_markup()


class BuyCallbackFactory(CallbackData, prefix="buy_cho_opt"):
    duration: int  # in days
    price: int
    extend: bool
    order_id: int
    back: bool = False


def get_payment_countries_keyboard(duration: int, price: int):
    builder = InlineKeyboardBuilder()
    for name, flag in COUNTRIES.items():
        builder.button(
            text=get_country_text(name, flag),
            callback_data=ChooseCountryCallbackFactory(
                option=Payment.Balance.value,
                duration=duration,
                price=price,
                country=name,
            ),
        )
    builder.button(
        text=back,
        callback_data=ChooseCountryCallbackFactory(
            option=Payment.Balance.value,
            duration=duration,
            price=price,
            country="",
            back=True,
        ),
    )
    builder.adjust(1)
    return builder.as_markup()


class ChooseCountryCallbackFactory(CallbackData, prefix="country"):
    option: int
    duration: int
    price: int
    country: str
    back: bool = False


def get_payment_options_keyboard(
    duration: int, price: int, country: str, extend: bool, order_id: int = -1
):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=card,
        callback_data=PaymentCallbackFactory(
            option=Payment.Card.value,
            duration=duration,
            price=price,
            country=country,
            extend=extend,
            order_id=order_id,
        ),
    )
    builder.button(
        text=balance,
        callback_data=PaymentCallbackFactory(
            option=Payment.Balance.value,
            duration=duration,
            price=price,
            country=country,
            extend=extend,
            order_id=order_id,
        ),
    )
    builder.button(
        text=back,
        callback_data=PaymentCallbackFactory(
            option=Payment.Back.value,
            duration=duration,
            price=price,
            country=country,
            extend=extend,
            order_id=order_id,
        ),
    )
    builder.adjust(1)
    return builder.as_markup()


class Payment(Enum):
    Balance = 0
    Card = 1
    Back = 2


class PaymentCallbackFactory(CallbackData, prefix="pay"):
    option: int
    duration: int
    price: int
    country: str
    extend: bool
    order_id: int


def get_balance_add_money_keyboard(
    duration: int, price: int, country: str, add: int, order_id: int = -1
):
    builder = InlineKeyboardBuilder()

    if add >= MIN_ADD_AMOUNT:
        builder.button(
            text=str(add),
            callback_data=PaymentAddMoneyCallbackFactory(
                duration=duration,
                price=price,
                country=country,
                amount=add,
                order_id=order_id,
            ),
        )
    else:
        builder.button(
            text=str(MIN_ADD_AMOUNT),
            callback_data=PaymentAddMoneyCallbackFactory(
                duration=duration,
                price=price,
                country=country,
                amount=MIN_ADD_AMOUNT,
                order_id=order_id,
            ),
        )

    adds = [100, 200, 300, 500, 1000, 2000]
    col = 0
    for amount in adds:
        if amount >= add:
            col += 1
            builder.button(
                text=str(amount),
                callback_data=PaymentAddMoneyCallbackFactory(
                    duration=duration,
                    price=price,
                    country=country,
                    amount=amount,
                    order_id=order_id,
                ),
            )
    builder.button(
        text=back,
        callback_data=PaymentAddMoneyCallbackFactory(
            duration=duration,
            price=price,
            country=country,
            amount=0,
            order_id=order_id,
            back=True,
        ),
    )
    builder.adjust(1, 3 if col >= 3 else col, col - 3 if col > 3 else 1, 1)
    return builder.as_markup()


class PaymentAddMoneyCallbackFactory(CallbackData, prefix="pay_add_money"):
    duration: int
    price: int
    amount: int
    country: str
    order_id: int
    back: bool = False
