from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.controllers.order import get_order, update_order
from database.controllers.user import get_user, register_user
from keyboards.buy import get_buy_vpn_keyboard, BuyCallbackFactory, PaymentCallbackFactory, Payment
from keyboards.info import (
    InfoBackCallbackFactory,
    InfoCallbackFactory,
    get_back_keyboard,
    get_info_keyboard, get_choose_order_keyboard, InfoChooseOrderCallbackFactory, get_my_keys_keyboard,
)
from keyboards.profile import get_profile_keyboard, get_order_countries_keyboard, OrderChangesCallbackFactory, \
    ChooseCountryChangeCallbackFactory, get_order_changes_keyboard, BackKeyInfoCallbackFactory
from schemas import OrderModel
from servers.outline_keys import get_key
from text.info import get_countries_text, get_referral_program_text, choose_order_to_change_country, get_no_orders_text, \
    choose_order_to_extend, expiration_date_text, auto_off_text, choose_order_to_off_auto, get_my_keys_text
from text.keyboard_text import (
    countries,
    referral_program, change_country, extend_key, back, off_auto, my_keys, profile,
)
from text.profile import get_order_choose_country_text, get_order_info_text, get_country_changed_text
from text.texts import (
    get_information_text, get_buy_vpn_text, get_profile_text,
)

info_router = Router(name="info")


@info_router.callback_query(InfoCallbackFactory.filter(F.text == profile))
async def info_profile_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    id = callback.message.from_user.id
    user = get_user(id)
    if user is None:
        register_user(id)
    await callback.message.edit_text(
        text=get_profile_text(id), reply_markup=get_profile_keyboard(id)
    )


@info_router.callback_query(InfoCallbackFactory.filter(F.text == my_keys))
async def info_my_keys_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.edit_text(
            text=get_no_orders_text() + get_information_text(),
            reply_markup=get_info_keyboard()
        )
    elif len(orders) == 1:
        await my_key(callback, order=orders[0])
    else:
        await callback.message.edit_text(
            text=get_my_keys_text(),
            reply_markup=get_choose_order_keyboard(orders)
        )
    await callback.answer()


async def my_key(callback: CallbackQuery, order: OrderModel):
    await callback.message.edit_text(
        text=get_order_info_text(order_id=order.id),
        reply_markup=get_my_keys_keyboard(off_auto_need=order.payment_id is not None and order.payment_id != "",
                                          order_id=order.id)
    )


@info_router.callback_query(InfoChooseOrderCallbackFactory.filter())
async def my_keys_callback(callback: CallbackQuery, callback_data: InfoChooseOrderCallbackFactory):
    order = get_order(callback_data.order_id)
    await my_key(callback, order=order)


@info_router.callback_query(InfoCallbackFactory.filter(F.text == back))
async def back_from_my_keys_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) <= 1:
        await callback.message.answer(
            text=get_information_text(), reply_markup=get_info_keyboard()
        )
    else:
        await info_my_keys_callback(callback, callback_data)
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == change_country))
async def info_change_country_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=get_order_choose_country_text(order.id, order.country),
        reply_markup=get_order_countries_keyboard(id=order.id),
    )


@info_router.callback_query(OrderChangesCallbackFactory.filter(F.text == back))
async def profile_back_order_info_country_callback(
        callback: CallbackQuery, callback_data: OrderChangesCallbackFactory
):
    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(
    ChooseCountryChangeCallbackFactory.filter(F.back == True)
)
async def changing_country_back_callback(
        callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    await my_key(callback, order=get_order(callback_data.id))
    await callback.answer()


@info_router.callback_query(
    ChooseCountryChangeCallbackFactory.filter(F.back == False)
)
async def changing_country_callback(
        callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    order = get_order(callback_data.id)
    update_order(order.id, {"country": callback_data.country})
    get_key(callback_data.country, order.id)
    await callback.message.edit_text(
        text=get_country_changed_text() + get_order_info_text(callback_data.id),
        reply_markup=get_order_changes_keyboard(order_id=order.id),
    )
    await callback.answer()


@info_router.callback_query(BackKeyInfoCallbackFactory.filter())
async def back_to_profile_callback(callback: CallbackQuery, callback_data: BackKeyInfoCallbackFactory):
    await callback.message.answer(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == extend_key))
async def extend_key_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=expiration_date_text(order) + get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=order.id, need_back=True
        ),
    )


@info_router.callback_query(
    PaymentCallbackFactory.filter((F.option == Payment.Back.value) & (F.extend == True))
)
async def buy_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
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
async def profile_extend_key_callback(
        callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.answer(get_no_orders_text())
    elif len(orders) == 1:
        await callback.message.answer(
            text=get_information_text(), reply_markup=get_info_keyboard()
        )
    else:
        await callback.message.edit_text(
            text=choose_order_to_extend(),
            reply_markup=get_choose_order_keyboard(orders, extend_key=True)
        )
    await callback.answer()


@info_router.callback_query(InfoChooseOrderCallbackFactory.filter(F.extend_key))
async def extend_key_prices_callback(
        callback: CallbackQuery, callback_data: InfoChooseOrderCallbackFactory
):
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=expiration_date_text(order) + get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=order.id, need_back=True
        ),
    )
    await callback.answer()


@info_router.callback_query(InfoBackCallbackFactory.filter())
async def back_to_info_start_callback(
        callback: CallbackQuery, callback_data: InfoBackCallbackFactory
):
    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == off_auto))
async def off_auto_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    order_id = callback_data.order_id
    update_order(order_id, {'payment_id': None})
    await callback.message.edit_text(
        text=auto_off_text(callback_data.order_id),
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
