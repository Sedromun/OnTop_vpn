import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.controllers.order import get_order, update_order
from database.controllers.user import get_user, register_user, update_user
from handlers import get_order_data
from keyboards.buy import (BuyCallbackFactory, Payment, PaymentCallbackFactory,
                           get_balance_add_money_keyboard,
                           get_buy_vpn_keyboard)
from keyboards.info import (InfoBackCallbackFactory, InfoCallbackFactory,
                            InfoChooseOrderCallbackFactory, get_back_keyboard,
                            get_choose_order_keyboard, get_info_keyboard,
                            get_my_keys_keyboard, get_profile_keyboard)
from keyboards.profile import (BackKeyInfoCallbackFactory,
                               ChooseCountryChangeCallbackFactory,
                               get_buy_vpn_from_notify_keyboard,
                               get_order_changes_keyboard,
                               get_order_countries_keyboard)
from logs import bot_logger
from schemas import OrderModel
from servers.outline_keys import get_key
from text.info import (auto_off_text, expiration_date_text, get_my_keys_text,
                       get_no_orders_text)
from text.keyboard_text import (back, change_country, extend_key, my_keys,
                                off_auto, profile)
from text.profile import (get_country_changed_text,
                          get_order_choose_country_text, get_order_info_text,
                          get_success_extended_key_text)
from text.texts import (get_buy_vpn_text, get_information_text,
                        get_not_enough_money_text, get_profile_text)
from utils.buy_options import duration_to_str
from utils.payment_handle import PaymentPurpose, buy_handle

info_router = Router(name="info")


# --- main buttons ---


@info_router.callback_query(InfoCallbackFactory.filter(F.text == profile))
async def info_profile_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.info_profile_callback")
    id = callback.from_user.id
    user = get_user(id)
    if user is None:
        register_user(id)
    await callback.message.edit_text(
        text=get_profile_text(id), reply_markup=get_profile_keyboard()
    )


@info_router.callback_query(InfoCallbackFactory.filter(F.text == my_keys))
async def info_my_keys_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.info_my_keys_callback")
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.edit_text(
            text=get_no_orders_text(),
            reply_markup=get_buy_vpn_from_notify_keyboard(),
        )
    elif len(orders) == 1:
        await my_key(callback, order=orders[0])
    else:
        await callback.message.edit_text(
            text=get_my_keys_text(), reply_markup=get_choose_order_keyboard(orders)
        )
    await callback.answer()


# --- my keys ---


async def my_key(callback: CallbackQuery, order: OrderModel):
    await callback.message.edit_text(
        text=get_order_info_text(order_id=order.id),
        reply_markup=get_my_keys_keyboard(
            off_auto_need=order.payment_id is not None and order.payment_id != "",
            order_id=order.id,
        ),
    )


@info_router.callback_query(InfoChooseOrderCallbackFactory.filter())
async def my_keys_callback(
    callback: CallbackQuery, callback_data: InfoChooseOrderCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.my_keys_callback")
    order = get_order(callback_data.order_id)
    await my_key(callback, order=order)


# --- my keys buttons ---


@info_router.callback_query(InfoCallbackFactory.filter(F.text == off_auto))
async def off_auto_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.off_auto_callback")
    order_id = callback_data.order_id
    update_order(order_id, {"payment_id": None})
    await callback.message.edit_text(
        text=auto_off_text(callback_data.order_id), reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == extend_key))
async def extend_key_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.extend_key_callback")
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=expiration_date_text(order) + get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=order.id, need_back=True
        ),
    )


@info_router.callback_query(InfoCallbackFactory.filter(F.text == change_country))
async def info_change_country_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.info_change_country_callback")
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=get_order_choose_country_text(order.id, order.country),
        reply_markup=get_order_countries_keyboard(id=order.id),
    )


@info_router.callback_query(InfoCallbackFactory.filter(F.text == back))
async def back_from_my_keys_callback(
    callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.back_from_my_keys_callback")
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) <= 1:
        await callback.message.edit_text(
            text=get_information_text(), reply_markup=get_info_keyboard()
        )
    else:
        await info_my_keys_callback(callback, callback_data)
    await callback.answer()


# --- change country ---


@info_router.callback_query(ChooseCountryChangeCallbackFactory.filter(F.back == False))
async def changing_country_callback(
    callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.changing_country_callback")
    order = get_order(callback_data.id)
    update_order(order.id, {"country": callback_data.country})
    get_key(callback_data.country, order.id)
    await callback.message.edit_text(
        text=get_country_changed_text(order.id),
        reply_markup=get_order_changes_keyboard(),
    )
    await callback.answer()


@info_router.callback_query(ChooseCountryChangeCallbackFactory.filter(F.back == True))
async def changing_country_back_callback(
    callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.changing_country_back_callback")
    await my_key(callback, order=get_order(callback_data.id))
    await callback.answer()


# --- extend key ---


@info_router.callback_query(
    PaymentCallbackFactory.filter((F.option == Payment.Back.value) & (F.extend == True))
)
async def buy_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    bot_logger.info(f"Callback: '{callback.id}' - info.buy_callback")
    order = get_order(callback_data.order_id)
    if order is None:
        await callback.answer("Время действия ключа истекло")
        await callback.message.delete()
        return
    await callback.message.edit_text(
        text=expiration_date_text(order) + get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=callback_data.order_id, need_back=True
        ),
    )
    await callback.answer()


@info_router.callback_query(BuyCallbackFactory.filter(F.back == True))
async def keys_back_from_extend_key_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - info.keys_back_from_extend_key_callback"
    )

    await my_key(callback, order=get_order(callback_data.order_id))
    await callback.answer()


# --- extend key --- payment ---
@info_router.callback_query(
    PaymentCallbackFactory.filter((F.option == Payment.Card.value) & (F.extend == True))
)
async def extend_card_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.extend_card_callback")

    order_data = get_order_data(callback, callback_data)

    await buy_handle(
        callback,
        callback_data,
        callback_data.price,
        order_id=callback_data.order_id,
        order_data=order_data,
        purpose=PaymentPurpose.EXTEND_CARD,
        title="Продление ключа",
        description=f"VPN - продление ({duration_to_str(callback_data.duration)})",
    )


@info_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Balance.value) & (F.extend == True)
    )
)
async def extend_balance_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.extend_balance_callback")

    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    order = get_order(callback_data.order_id)
    if order is None:
        await callback.answer("Время действия ключа истекло")
        await callback.message.delete()
        return
    if user.balance >= callback_data.price:
        update_user(
            callback.from_user.id, {"balance": user.balance - callback_data.price}
        )
        begin = order.expiration_date
        end = begin + datetime.timedelta(days=callback_data.duration)
        update_order(order.id, {"expiration_date": end})
        await callback.message.edit_text(
            text=get_success_extended_key_text() + get_order_info_text(order.id)
        )
    else:
        await callback.message.edit_text(
            text=get_not_enough_money_text(callback_data.price - user.balance),
            reply_markup=get_balance_add_money_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country=callback_data.country,
                add=callback_data.price - user.balance,
                order_id=callback_data.order_id,
            ),
        )
    await callback.answer()


#  --- back callbacks ---


@info_router.callback_query(InfoBackCallbackFactory.filter())
async def back_to_info_start_callback(
    callback: CallbackQuery, callback_data: InfoBackCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.back_to_info_start_callback")

    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(BackKeyInfoCallbackFactory.filter())
async def back_to_profile_callback(
    callback: CallbackQuery, callback_data: BackKeyInfoCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - info.back_to_profile_callback")

    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()
