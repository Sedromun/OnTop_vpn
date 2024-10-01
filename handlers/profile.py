import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.controllers.order import get_order, update_order
from database.controllers.user import get_user, update_user, register_user
from keyboards.buy import (
    BuyCallbackFactory,
    Payment,
    PaymentAddMoneyCallbackFactory,
    PaymentCallbackFactory,
    get_balance_add_money_keyboard,
    get_buy_vpn_keyboard,
    get_payment_options_keyboard,
)
from keyboards.profile import (
    ChooseCountryChangeCallbackFactory,
    OrderChangesCallbackFactory,
    ProfileAddMoneyCallbackFactory,
    ProfileCallbackFactory,
    get_add_money_keyboard,
    get_order_changes_keyboard,
    get_order_countries_keyboard,
    get_profile_keyboard, OrderExpiringCallbackFactory,
)
from servers.outline_keys import get_key
from text.keyboard_text import back, change_country, extend_key
from text.profile import (
    get_country_changed_text,
    get_order_choose_country_text,
    get_order_info_text,
    get_profile_add_money_text,
    get_success_extended_key_text,
)
from text.texts import (
    get_buy_vpn_text,
    get_not_enough_money_text,
    get_payment_option_text,
    get_profile_text,
)
from utils.buy_options import duration_to_str
from utils.payment_handle import buy_handle

profile_router = Router(name="profile")


@profile_router.callback_query(ProfileCallbackFactory.filter(F.balance == False))
async def profile_order_info_callback(
    callback: CallbackQuery, callback_data: ProfileCallbackFactory
):
    await callback.message.edit_text(
        text=get_order_info_text(callback_data.order_id),
        reply_markup=get_order_changes_keyboard(callback_data.order_id),
    )
    await callback.answer()


@profile_router.callback_query(
    OrderChangesCallbackFactory.filter(F.text == change_country)
)
async def profile_change_country_callback(
    callback: CallbackQuery, callback_data: OrderChangesCallbackFactory
):
    order = get_order(callback_data.id)
    await callback.message.edit_text(
        text=get_order_choose_country_text(order.country),
        reply_markup=get_order_countries_keyboard(id=order.id),
    )
    await callback.answer()


@profile_router.callback_query(OrderChangesCallbackFactory.filter(F.text == back))
async def profile_back_order_info_country_callback(
    callback: CallbackQuery, callback_data: OrderChangesCallbackFactory
):
    id = callback.from_user.id
    await callback.message.edit_text(
        text=get_profile_text(id), reply_markup=get_profile_keyboard(id)
    )
    await callback.answer()


@profile_router.callback_query(OrderChangesCallbackFactory.filter(F.text == extend_key))
async def profile_extend_key_callback(
    callback: CallbackQuery, callback_data: OrderChangesCallbackFactory
):
    await callback.message.edit_text(
        text=get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=callback_data.id, need_back=True
        ),
    )
    await callback.answer()


@profile_router.callback_query(BuyCallbackFactory.filter(F.back == True))
async def profile_extend_key_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    await callback.message.edit_text(
        text=get_order_info_text(callback_data.order_id),
        reply_markup=get_order_changes_keyboard(callback_data.order_id),
    )
    await callback.answer()


@profile_router.callback_query(
    BuyCallbackFactory.filter((F.extend == True) & (F.back == False))
)
async def profile_extend_key_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    if callback.message.photo is not None:
        await callback.message.edit_text(
            text=get_payment_option_text(callback_data.price, user.balance),
            reply_markup=get_payment_options_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country="",
                extend=True,
                order_id=callback_data.order_id,
            ),
        )
    else:
        order = get_order(callback_data.order_id)
        if order is None:
            await callback.answer("Время действия ключа истекло")
            await callback.message.delete()
            return
        await callback.message.edit_text(
            text=get_payment_option_text(callback_data.price, user.balance),
            reply_markup=get_payment_options_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country="",
                extend=True,
                order_id=callback_data.order_id,
            ),
        )
    await callback.answer()


@profile_router.callback_query(
    PaymentCallbackFactory.filter((F.option == Payment.Back.value) & (F.extend == True))
)
async def buy_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    if callback.message.photo is not None:
        await callback.message.edit_text(
            text=get_buy_vpn_text(),
            reply_markup=get_buy_vpn_keyboard(
                extend=True, order_id=callback_data.order_id, need_back=True
            ),
        )
    else:
        order = get_order(callback_data.order_id)
        if order is None:
            await callback.answer("Время действия ключа истекло")
            await callback.message.delete()
            return
        await callback.message.edit_text(
            text=get_buy_vpn_text(),
            reply_markup=get_buy_vpn_keyboard(
                extend=True, order_id=callback_data.order_id, need_back=True
            ),
        )
    await callback.answer()


@profile_router.callback_query(
    PaymentCallbackFactory.filter((F.option == Payment.Card.value) & (F.extend == True))
)
async def buy_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    await buy_handle(
        callback,
        callback_data,
        callback_data.price,
        order_id=callback_data.order_id,
        extend=True,
        title="Продление ключа",
        description=f"VPN - продление ({duration_to_str(callback_data.duration)})"
    )


@profile_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Balance.value) & (F.extend == True)
    )
)
async def buy_balance_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
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
        if callback.message.photo is not None:
            await callback.message.edit_text(text=get_success_extended_key_text())
        else:
            await callback.message.edit_text(text=get_success_extended_key_text())
    else:
        if callback.message.photo is not None:
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


@profile_router.callback_query(
    PaymentAddMoneyCallbackFactory.filter((F.order_id != -1) & (F.back == True))
)
async def add_money_balance_back_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    order = get_order(callback_data.order_id)
    if order is None:
        await callback.answer("Время действия ключа истекло")
        await callback.message.delete()
        return
    if callback.message.photo is not None:
        await callback.message.edit_text(
            text=get_payment_option_text(callback_data.price, user.balance),
            reply_markup=get_payment_options_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country="",
                extend=True,
                order_id=callback_data.order_id,
            ),
        )
    else:
        await callback.message.edit_text(
            text=get_payment_option_text(callback_data.price, user.balance),
            reply_markup=get_payment_options_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country="",
                extend=True,
                order_id=callback_data.order_id,
            ),
        )
    await callback.answer()


@profile_router.callback_query(PaymentAddMoneyCallbackFactory.filter(F.order_id != -1))
async def add_money_balance_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    await buy_handle(
        callback,
        callback_data,
        callback_data.amount,
        callback_data.order_id,
        extend=True,
        title="Пополнение баланса",
        description=f"Продление ключа VPN ({duration_to_str(callback_data.duration)})"
    )


@profile_router.callback_query(
    ChooseCountryChangeCallbackFactory.filter(F.back == True)
)
async def changing_country_back_callback(
    callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    await callback.message.edit_text(
        text=get_order_info_text(callback_data.id),
        reply_markup=get_order_changes_keyboard(callback_data.id),
    )
    await callback.answer()


@profile_router.callback_query(
    ChooseCountryChangeCallbackFactory.filter(F.back == False)
)
async def changing_country_callback(
    callback: CallbackQuery, callback_data: ChooseCountryChangeCallbackFactory
):
    order = get_order(callback_data.id)
    update_order(order.id, {"country": callback_data.country})
    get_key(callback_data.country, order.id)
    await callback.message.edit_text(
        text=get_country_changed_text()
        + get_order_info_text(callback_data.id),
        reply_markup=get_order_changes_keyboard(callback_data.id),
    )
    await callback.answer()


@profile_router.callback_query(ProfileCallbackFactory.filter(F.balance == True))
async def profile_order_info_callback(
    callback: CallbackQuery, callback_data: ProfileCallbackFactory
):
    await callback.message.edit_text(
        text=get_profile_add_money_text(),
        reply_markup=get_add_money_keyboard(),
    )
    await callback.answer()


@profile_router.callback_query(ProfileAddMoneyCallbackFactory.filter(F.back == True))
async def add_money_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    id = callback.from_user.id

    await callback.message.edit_text(
        text=get_profile_text(id), reply_markup=get_profile_keyboard(id)
    )
    await callback.answer()


@profile_router.callback_query(ProfileAddMoneyCallbackFactory.filter(F.back == False))
async def add_money_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    await buy_handle(
        callback,
        callback_data,
        callback_data.amount,
        0,
        add_money=True,
        title="Пополнение баланса",
        description=f"Баланс - аккаунт ID: {callback.from_user.id}"
    )


@profile_router.callback_query(OrderExpiringCallbackFactory.filter())
async def profile_extend_expiring_key_callback(
    callback: CallbackQuery, callback_data: OrderExpiringCallbackFactory
):
    order = get_order(callback_data.id)
    if order is None:
        await callback.answer("Время действия ключа истекло")
        await callback.message.delete()
        return

    await callback.message.edit_text(
        text=get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(
            extend=True, order_id=callback_data.id, need_back=False
        ),
    )
    await callback.answer()

