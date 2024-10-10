import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, PreCheckoutQuery
from yookassa import Payment as YookassaPayment

from database.controllers.order import create_order, get_order
from database.controllers.user import get_user, register_user, update_user
from keyboards.buy import (BackFromPaymentCallbackFactory, BuyCallbackFactory,
                           ChooseCountryCallbackFactory, Payment,
                           PaymentAddMoneyCallbackFactory,
                           PaymentCallbackFactory,
                           get_balance_add_money_keyboard,
                           get_buy_vpn_keyboard,
                           get_payment_countries_keyboard,
                           get_payment_options_keyboard)
from keyboards.info import get_instruction_button_keyboard
from logs import bot_logger
from servers.outline_keys import get_key
from text.profile import get_order_info_text
from text.texts import (get_buy_vpn_text, get_not_enough_money_text,
                        get_payment_choose_country_text,
                        get_payment_option_text, get_success_created_key_text)
from utils.buy_options import duration_to_str
from utils.payment import get_order_perm_key
from utils.payment_handle import PaymentPurpose, buy_handle, check_not_payed

buy_router = Router(name="buy")


@buy_router.callback_query(BuyCallbackFactory.filter(F.extend == False))
async def choose_country_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.choose_country_callback")
    await callback.message.edit_text(
        text=get_payment_choose_country_text(),
        reply_markup=get_payment_countries_keyboard(
            duration=callback_data.duration, price=callback_data.price
        ),
    )
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == True))
async def choose_payment_back_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.choose_payment_back_callback")
    await callback.message.edit_text(
        text=get_buy_vpn_text(), reply_markup=get_buy_vpn_keyboard(extend=False, user_id=callback.from_user.id)
    )
    await callback.answer()


@buy_router.callback_query(ChooseCountryCallbackFactory.filter(F.back == False))
async def choose_payment_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.choose_payment_callback")
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
    if callback_data.price == 0:
        user = get_user(callback.from_user.id)
        if user.present:
            await callback.message.delete()
            await callback.answer()
            return

        update_user(callback.from_user.id, {"present": True})
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
            text=get_success_created_key_text(get_order_perm_key(order.id))
            + get_order_info_text(order.id),
            reply_markup=get_instruction_button_keyboard(),
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
async def buy_balance_back_callback(
    callback: CallbackQuery, callback_data: PaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.buy_balance_back_callback")
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
    bot_logger.info(f"Callback: '{callback.id}' - buy.buy_balance_callback")
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
                "price": callback_data.price,
            }
        )
        key = get_key(callback_data.country, order.id)
        update_user(
            callback.from_user.id, {"balance": user.balance - callback_data.price}
        )

        await callback.message.edit_text(
            text=get_success_created_key_text(get_order_perm_key(order.id))
            + get_order_info_text(order.id),
            reply_markup=get_instruction_button_keyboard(),
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
async def add_money_back_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.add_money_back_callback")
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
    bot_logger.info(f"Callback: '{callback.id}' - buy.add_money_callback")
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


@buy_router.callback_query(
    PaymentCallbackFactory.filter(
        (F.option == Payment.Card.value) & (F.extend == False)
    )
)
async def buy_card_callback(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    bot_logger.info(f"Callback: '{callback.id}' - buy.buy_card_callback")
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
    return {
        "user_id": callback.from_user.id,
        "country": callback_data.country,
        "duration": callback_data.duration,
        "price": callback_data.price,
    }


@buy_router.callback_query(
    BackFromPaymentCallbackFactory.filter(F.purpose == PaymentPurpose.BUY_CARD.value)
)
async def back_from_payment_buy_card_callback(
    callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.back_from_payment_buy_card_callback")
    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_payment_option_text(int(data["price"]), user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=int(data["duration"]),
            price=int(data["price"]),
            country=data["country"],
            extend=False,
        ),
    )

    await callback.answer()


@buy_router.callback_query(
    BackFromPaymentCallbackFactory.filter(
        F.purpose == PaymentPurpose.BUY_ADD_MONEY.value
    )
)
async def back_from_payment_add_money_callback(
    callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - buy.back_from_payment_add_money_callback")
    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_not_enough_money_text(int(data["price"]) - user.balance),
        reply_markup=get_balance_add_money_keyboard(
            duration=int(data["duration"]),
            price=int(data["price"]),
            country=data["country"],
            add=int(data["price"]) - user.balance,
        ),
    )

    await callback.answer()
