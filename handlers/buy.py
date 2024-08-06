import datetime

from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from aiogram import F, Router, types

from config import dp, bot, PAYMENTS_PROVIDER_TOKEN
from database.controllers.order import create_order, get_order, update_order
from database.controllers.user import get_user, update_user
from keyboards.buy import BuyCallbackFactory, get_payment_options_keyboard, PaymentCallbackFactory, Payment, \
    get_payment_countries_keyboard, get_buy_vpn_keyboard, get_balance_add_money_keyboard, \
    PaymentAddMoneyCallbackFactory, ChooseCountryCallbackFactory
from servers.outline_keys import get_key
from text.keyboard_text import buy
from text.profile import get_success_extended_key_text, get_money_added_text
from text.texts import get_payment_option_text, get_success_created_key_text, get_payment_choose_country_text, \
    get_buy_vpn_text, get_not_enough_money_text, get_pay_text
from utils.payment import buy_handle

buy_router = Router(name="buy")


@buy_router.callback_query(BuyCallbackFactory.filter(F.extend == False))
async def choose_country_callback(
        callback: CallbackQuery,
        callback_data: BuyCallbackFactory
):
    await callback.message.edit_text(
        text=get_payment_choose_country_text(),
        reply_markup=get_payment_countries_keyboard(duration=callback_data.duration, price=callback_data.price),
    )
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == True))
async def choose_payment_callback(
        callback: CallbackQuery,
        callback_data: PaymentCallbackFactory
):
    await callback.message.edit_text(text=get_buy_vpn_text(), reply_markup=get_buy_vpn_keyboard(extend=False))
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == False))
async def choose_payment_callback(
        callback: CallbackQuery,
        callback_data: PaymentCallbackFactory
):
    user = get_user(callback.from_user.id)
    await callback.message.edit_text(
        text=get_payment_option_text(callback_data.price, user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=callback_data.duration,
            price=callback_data.price,
            country=callback_data.country,
            extend=False
        )
    )
    await callback.answer()


@buy_router.callback_query(PaymentCallbackFactory.filter((F.option == Payment.Back.value) & (F.extend == False)))
async def buy_balance_callback(
        callback: CallbackQuery,
        callback_data: PaymentCallbackFactory
):
    await callback.message.edit_text(
        text=get_payment_choose_country_text(),
        reply_markup=get_payment_countries_keyboard(duration=callback_data.duration, price=callback_data.price),
    )
    await callback.answer()


@buy_router.callback_query(PaymentCallbackFactory.filter((F.option == Payment.Balance.value) & (F.extend == False)))
async def buy_balance_callback(
        callback: CallbackQuery,
        callback_data: PaymentCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user.balance >= callback_data.price:
        key = get_key(callback_data.country)
        update_user(callback.from_user.id, {'balance': user.balance - callback_data.price})
        begin = datetime.datetime.now()
        end = begin + datetime.timedelta(days=callback_data.duration)
        create_order({
            'user_id': user.id,
            'country': callback_data.country,
            'begin_date': begin,
            'expiration_date': end,
            'key': key
        })

        await callback.message.edit_text(
            text=get_success_created_key_text(key)
        )

        return
    else:
        await callback.message.edit_text(
            text=get_not_enough_money_text(callback_data.price - user.balance),
            reply_markup=get_balance_add_money_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country=callback_data.country,
                add=callback_data.price - user.balance
            )
        )
    await callback.answer()


@buy_router.callback_query(PaymentAddMoneyCallbackFactory.filter((F.order_id == -1) & (F.back == True)))
async def add_money_callback(
        callback: CallbackQuery,
        callback_data: PaymentAddMoneyCallbackFactory
):
    user = get_user(callback.from_user.id)
    await callback.message.edit_text(
        text=get_payment_option_text(callback_data.price, user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=callback_data.duration,
            price=callback_data.price,
            country=callback_data.country,
            extend=False
        )
    )
    await callback.answer()


@buy_router.callback_query(PaymentAddMoneyCallbackFactory.filter((F.order_id == -1) & (F.back == False)))
async def add_money_callback(
        callback: CallbackQuery,
        callback_data: PaymentAddMoneyCallbackFactory
):
    order = create_new_order(callback, callback_data)
    await buy_handle(callback, callback_data, callback_data.amount, order.id)


@buy_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@buy_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    extend, order_id, duration_str = payload.split('_')
    user = get_user(message.from_user.id)
    amount = message.successful_payment.total_amount // 100

    if extend == 'E' or extend == 'C':
        order = get_order(int(order_id))
        price = order.price
        new_balance = user.balance + amount - price
        update_user(user.id, {'balance': new_balance})
        if extend == 'C':
            key = get_key(order.country)
            update_order(order.id, {'key': key})
            await message.answer(
                text=get_success_created_key_text(key)
            )
        else:
            begin = order.expiration_date
            end = begin + datetime.timedelta(days=int(duration_str))
            update_order(order.id, {'expiration_date': end})

            await message.answer(
                text=get_success_extended_key_text()
            )
    else:
        new_balance = user.balance + amount
        update_user(message.from_user.id, {'balance': new_balance})
        await message.answer(
            text=get_money_added_text()
        )


@buy_router.callback_query(PaymentCallbackFactory.filter((F.option == Payment.Card.value) & (F.extend == False)))
async def buy_callback(
        callback: CallbackQuery,
        callback_data: PaymentCallbackFactory
):
    order = create_new_order(callback, callback_data)
    await buy_handle(callback, callback_data, callback_data.price, order.id)


def create_new_order(callback, callback_data):
    begin = datetime.datetime.now()
    end = begin + datetime.timedelta(days=callback_data.duration)
    return create_order({
        'user_id': callback.from_user.id,
        'country': callback_data.country,
        'begin_date': begin,
        'expiration_date': end,
        'price': callback_data.price
    })
