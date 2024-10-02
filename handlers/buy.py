import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, PreCheckoutQuery

from yookassa import Payment as YookassaPayment


from database.controllers.order import create_order, get_order, delete_order
from database.controllers.user import get_user, update_user, register_user
from keyboards.buy import (
    BuyCallbackFactory,
    ChooseCountryCallbackFactory,
    Payment,
    PaymentAddMoneyCallbackFactory,
    PaymentCallbackFactory,
    get_balance_add_money_keyboard,
    get_buy_vpn_keyboard,
    get_payment_countries_keyboard,
    get_payment_options_keyboard, BackFromPaymentCallbackFactory,
)
from servers.outline_keys import get_key
from text.profile import get_order_info_text
from text.texts import (
    get_buy_vpn_text,
    get_not_enough_money_text,
    get_payment_choose_country_text,
    get_payment_option_text,
    get_success_created_key_text,
)
from utils.buy_options import duration_to_str
from utils.payment import get_order_perm_key
from utils.payment_handle import buy_handle, PaymentPurpose, check_not_payed

buy_router = Router(name="buy")


@buy_router.callback_query(BuyCallbackFactory.filter(F.extend == False))
async def choose_country_callback(
        callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    await callback.message.edit_text(
        text=get_payment_choose_country_text(),
        reply_markup=get_payment_countries_keyboard(
            duration=callback_data.duration, price=callback_data.price
        ),
    )
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == True))
async def choose_payment_callback(
        callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    await callback.message.edit_text(
        text=get_buy_vpn_text(), reply_markup=get_buy_vpn_keyboard(extend=False)
    )
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == False))
async def choose_payment_callback(
        callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    if callback_data.price == 0:
        if not user.present:
            await callback.message.delete()
            return

        update_user(callback.from_user.id, {'present': True})
        begin = datetime.datetime.now(datetime.timezone.utc)
        end = begin + datetime.timedelta(days=callback_data.duration)
        order = create_order(
            {
                "user_id": user.id,
                "country": callback_data.country,
                "begin_date": begin,
                "expiration_date": end,
            }
        )
        get_key(callback_data.country, order.id)
        await callback.message.edit_text(
            text=get_success_created_key_text(get_order_perm_key(order.id)) + get_order_info_text(order.id)
        )
    else:
        await callback.message.edit_text(
            text=get_payment_option_text(callback_data.price, user.balance),
            reply_markup=get_payment_options_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country=callback_data.country,
                extend=False,
            ),
        )
    await callback.answer()


@buy_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Back.value) & (F.extend == False)
    )
)
async def buy_balance_callback(
        callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    await callback.message.edit_text(
        text=get_payment_choose_country_text(),
        reply_markup=get_payment_countries_keyboard(
            duration=callback_data.duration, price=callback_data.price
        ),
    )
    await callback.answer()


@buy_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Balance.value) & (F.extend == False)
    )
)
async def buy_balance_callback(
        callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    if user.balance >= callback_data.price:
        begin = datetime.datetime.now(datetime.timezone.utc)
        end = begin + datetime.timedelta(days=callback_data.duration)
        order = create_order(
            {
                "user_id": user.id,
                "country": callback_data.country,
                "begin_date": begin,
                "expiration_date": end,
                "price": callback_data.price
            }
        )
        key = get_key(callback_data.country, order.id)
        update_user(
            callback.from_user.id, {"balance": user.balance - callback_data.price}
        )

        await callback.message.edit_text(
            text=get_success_created_key_text(get_order_perm_key(order.id)) + get_order_info_text(order.id)
        )

        return
    else:
        await callback.message.edit_text(
            text=get_not_enough_money_text(callback_data.price - user.balance),
            reply_markup=get_balance_add_money_keyboard(
                duration=callback_data.duration,
                price=callback_data.price,
                country=callback_data.country,
                add=callback_data.price - user.balance,
            ),
        )
    await callback.answer()


@buy_router.callback_query(
    PaymentAddMoneyCallbackFactory.filter((F.order_id == -1) & (F.back == True))
)
async def add_money_callback(
        callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    await callback.message.edit_text(
        text=get_payment_option_text(callback_data.price, user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=callback_data.duration,
            price=callback_data.price,
            country=callback_data.country,
            extend=False,
        ),
    )
    await callback.answer()


@buy_router.callback_query(
    PaymentAddMoneyCallbackFactory.filter((F.order_id == -1) & (F.back == False))
)
async def add_money_callback(
        callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    order_data = get_order_data(callback, callback_data)
    await buy_handle(
        callback,
        callback_data,
        callback_data.amount,
        purpose=PaymentPurpose.BUY_ADD_MONEY,
        title="Пополнение баланса",
        description="Покупка VPN - " + duration_to_str(callback_data.duration),
        order_data=order_data,
    )


@buy_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@buy_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Card.value) & (F.extend == False)
    )
)
async def buy_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    order_data = get_order_data(callback, callback_data)
    await buy_handle(
        callback,
        callback_data,
        callback_data.price,
        purpose=PaymentPurpose.BUY_CARD,
        title="VPN",
        description=f"Покупка VPN - {duration_to_str(callback_data.duration)}",
        order_data=order_data,
    )


def get_order_data(callback, callback_data) -> dict:
    # begin = datetime.datetime.now(datetime.timezone.utc)
    # end = begin + datetime.timedelta(days=callback_data.duration)
    return {
            "user_id": callback.from_user.id,
            "country": callback_data.country,
            "duration": callback_data.duration,
            "price": callback_data.price,
        }


@buy_router.callback_query(
    BackFromPaymentCallbackFactory.filter(
        F.purpose == PaymentPurpose.BUY_CARD.value
    )
)
async def back_from_payment_callback(callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory):
    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_payment_option_text(int(data['price']), user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=int(data['duration']),
            price=int(data['price']),
            country=data['country'],
            extend=False,
        ),
    )

    await callback.answer()


@buy_router.callback_query(
    BackFromPaymentCallbackFactory.filter(
        F.purpose == PaymentPurpose.BUY_ADD_MONEY.value
    )
)
async def back_from_payment_callback(callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory):
    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_not_enough_money_text(int(data['price']) - user.balance),
        reply_markup=get_balance_add_money_keyboard(
            duration=int(data['duration']),
            price=int(data['price']),
            country=data['country'],
            add=int(data['price']) - user.balance,
        ),
    )

    await callback.answer()
