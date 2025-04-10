from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import INSTR_URL, RECALLS_TGC_LINK, TECH_SUPPORT_LINK
from schemas import OrderModel
from text.keyboard_text import (all_instr, back, change_country, extend_key,
                                get_order_short_text, my_keys, off_auto,
                                profile, recalls, tech_support, top_up_balance)


def get_info_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=my_keys, callback_data=InfoCallbackFactory(text=my_keys))
    builder.button(text=profile, callback_data=InfoCallbackFactory(text=profile))
    builder.button(text=all_instr, url=INSTR_URL)
    builder.button(text=tech_support, url=TECH_SUPPORT_LINK)
    builder.button(text=recalls, url=RECALLS_TGC_LINK)
    builder.adjust(1)
    return builder.as_markup()


class InfoCallbackFactory(CallbackData, prefix="info"):
    text: str
    order_id: int = -1


def get_my_keys_keyboard(off_auto_need: bool, order_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=change_country,
        callback_data=InfoCallbackFactory(text=change_country, order_id=order_id),
    )
    builder.button(
        text=extend_key,
        callback_data=InfoCallbackFactory(text=extend_key, order_id=order_id),
    )
    if off_auto_need:
        builder.button(
            text=off_auto,
            callback_data=InfoCallbackFactory(text=off_auto, order_id=order_id),
        )
    builder.button(
        text=back, callback_data=InfoCallbackFactory(text=back, order_id=order_id)
    )
    builder.adjust(1)
    return builder.as_markup()


def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=back, callback_data=InfoBackCallbackFactory(back=True))
    builder.adjust(1)
    return builder.as_markup()


class InfoBackCallbackFactory(CallbackData, prefix="info_back"):
    back: bool


def get_choose_order_keyboard(orders: [OrderModel]):
    builder = InlineKeyboardBuilder()

    for order in orders:
        builder.button(
            text=get_order_short_text(order.id, order.country),
            callback_data=InfoChooseOrderCallbackFactory(order_id=order.id),
        )

    builder.button(text=back, callback_data=InfoBackCallbackFactory(back=True))
    builder.adjust(1)
    return builder.as_markup()


class InfoChooseOrderCallbackFactory(CallbackData, prefix="info_cb"):
    order_id: int


def get_instruction_button_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=all_instr, url=INSTR_URL)
    builder.adjust(1)
    return builder.as_markup()


def get_profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=top_up_balance,
        callback_data=ProfileCallbackFactory(),
    )
    builder.button(
        text=back,
        callback_data=InfoBackCallbackFactory(back=True),
    )
    builder.adjust(1)
    return builder.as_markup()


class ProfileCallbackFactory(CallbackData, prefix="profile"):
    pass
