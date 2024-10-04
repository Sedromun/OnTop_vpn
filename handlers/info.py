from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.controllers.order import get_order, update_order
from database.controllers.user import get_user
from keyboards.buy import get_buy_vpn_keyboard, BuyCallbackFactory
from keyboards.info import (
    InfoBackCallbackFactory,
    InfoCallbackFactory,
    get_back_keyboard,
    get_info_keyboard, get_choose_order_keyboard, InfoChooseOrderCallbackFactory,
)
from keyboards.profile import get_profile_keyboard, get_order_countries_keyboard, OrderChangesCallbackFactory, \
    ChooseCountryChangeCallbackFactory, get_order_changes_keyboard, BackKeyInfoCallbackFactory
from servers.outline_keys import get_key
from text.info import get_countries_text, get_referral_program_text, choose_order_to_change_country, get_no_orders_text, \
    choose_order_to_extend, expiration_date_text
from text.keyboard_text import (
    countries,
    referral_program, change_country, extend_key, back,
)
from text.profile import get_order_choose_country_text, get_order_info_text, get_country_changed_text
from text.texts import (
    get_information_text, get_buy_vpn_text,
)

info_router = Router(name="info")


@info_router.callback_query(InfoCallbackFactory.filter(F.text == countries))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    await callback.message.edit_text(
        text=get_countries_text(), reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == referral_program))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    await callback.message.edit_text(
        text=get_referral_program_text(callback.from_user.id), reply_markup=get_back_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == change_country))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.answer(get_no_orders_text())
    elif len(orders) == 1:
        order = get_order(orders[0].id)
        await callback.message.edit_text(
            text=get_order_choose_country_text(order.id, order.country),
            reply_markup=get_order_countries_keyboard(id=order.id),
        )
    else:
        await callback.message.edit_text(
            text=choose_order_to_change_country(),
            reply_markup=get_choose_order_keyboard(callback.from_user.id, change_country=True)
        )
    await callback.answer()


@info_router.callback_query(OrderChangesCallbackFactory.filter(F.text == back))
async def profile_back_order_info_country_callback(
        callback: CallbackQuery, callback_data: OrderChangesCallbackFactory
):
    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoChooseOrderCallbackFactory.filter(F.change_country))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoChooseOrderCallbackFactory
):
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=get_order_choose_country_text(order.id, order.country),
        reply_markup=get_order_countries_keyboard(id=order.id),
    )


@info_router.callback_query(
    ChooseCountryChangeCallbackFactory.filter(F.back == True)
)
async def changing_country_back_callback(
        callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.edit_text(get_no_orders_text())
    elif len(orders) == 1:
        await callback.message.edit_text(
            text=get_information_text(), reply_markup=get_info_keyboard()
        )
    else:
        await callback.message.edit_text(
            text=choose_order_to_change_country(),
            reply_markup=get_choose_order_keyboard(callback.from_user.id, change_country=True)
        )
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
        reply_markup=get_order_changes_keyboard(order_id=order.id, info=True),
    )
    await callback.answer()


@info_router.callback_query(BackKeyInfoCallbackFactory.filter(F.info == True))
async def back_to_profile_callback(callback: CallbackQuery, callback_data: BackKeyInfoCallbackFactory):
    order = get_order(callback_data.order_id)
    await callback.message.edit_text(
        text=get_order_choose_country_text(order.id, order.country),
        reply_markup=get_order_countries_keyboard(id=order.id),
    )
    await callback.answer()


@info_router.callback_query(BackKeyInfoCallbackFactory.filter(F.back == True))
async def back_to_profile_callback(callback: CallbackQuery, callback_data: BackKeyInfoCallbackFactory):
    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoCallbackFactory.filter(F.text == extend_key))
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoCallbackFactory
):
    user = get_user(callback.from_user.id)
    orders = user.orders
    if len(orders) == 0:
        await callback.message.answer(get_no_orders_text())
    elif len(orders) == 1:
        await callback.message.edit_text(
            text=expiration_date_text(orders[0]) + get_buy_vpn_text(),
            reply_markup=get_buy_vpn_keyboard(
                extend=True, order_id=orders[0].id, need_back=True
            ),
        )
    else:
        await callback.message.edit_text(
            text=choose_order_to_extend(),
            reply_markup=get_choose_order_keyboard(callback.from_user.id, extend_key=True)
        )
    await callback.answer()


@info_router.callback_query(BuyCallbackFactory.filter(F.back == True))
async def profile_extend_key_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    await callback.message.answer(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()


@info_router.callback_query(InfoChooseOrderCallbackFactory.filter(F.extend_key))
async def info_countries_callback(
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
async def info_countries_callback(
        callback: CallbackQuery, callback_data: InfoBackCallbackFactory
):
    await callback.message.edit_text(
        text=get_information_text(), reply_markup=get_info_keyboard()
    )
    await callback.answer()
