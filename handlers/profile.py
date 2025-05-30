import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.controllers.order import get_order
from database.controllers.user import get_user, register_user, update_user
from handlers import get_order_data
from keyboards.buy import (BackFromPaymentCallbackFactory, BuyCallbackFactory,
                           PaymentAddMoneyCallbackFactory,
                           get_balance_add_money_keyboard,
                           get_buy_vpn_keyboard, get_payment_options_keyboard)
from keyboards.info import ProfileCallbackFactory, get_profile_keyboard
from keyboards.profile import (BuyVPNFromNotificationCallbackFactory,
                               InfoVPNNotificationCallbackFactory,
                               OrderExpiringCallbackFactory,
                               ProfileAddMoneyCallbackFactory,
                               get_add_money_keyboard,
                               get_buy_vpn_from_notify_keyboard)
from logs import bot_logger
from text.keyboard_text import bad_price, forgot_buy
from text.notifications import (bad_price_text, forgot_buy_text,
                                thanks_for_review_text)
from text.profile import get_profile_add_money_text
from text.texts import (get_buy_vpn_text, get_not_enough_money_text,
                        get_payment_option_text, get_profile_text)
from utils.buy_options import duration_to_str
from utils.payment_handle import PaymentPurpose, buy_handle, check_not_payed

profile_router = Router(name="profile")


# ---- extend key from notification ---
@profile_router.callback_query(
    BuyCallbackFactory.filter((F.extend == True) & (F.back == False))
)
async def profile_extend_key_callback(
    callback: CallbackQuery, callback_data: BuyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.profile_extend_key_callback")
    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
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


# --- extend key ----


@profile_router.callback_query(
    PaymentAddMoneyCallbackFactory.filter((F.order_id != -1) & (F.back == True))
)
async def add_money_balance_back_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - profile.add_money_balance_back_callback"
    )

    user = get_user(callback.from_user.id)
    if user is None:
        register_user(callback.from_user.id)
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


@profile_router.callback_query(PaymentAddMoneyCallbackFactory.filter(F.order_id != -1))
async def add_money_balance_callback(
    callback: CallbackQuery, callback_data: PaymentAddMoneyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.add_money_balance_callback")

    order_data = get_order_data(callback, callback_data)

    await buy_handle(
        callback,
        callback_data,
        callback_data.amount,
        purpose=PaymentPurpose.EXTEND_ADD_MONEY,
        title="Пополнение баланса",
        description=f"Продление ключа VPN ({duration_to_str(callback_data.duration)})",
        order_id=callback_data.order_id,
        order_data=order_data,
    )


@profile_router.callback_query(
    BackFromPaymentCallbackFactory.filter(F.purpose == PaymentPurpose.EXTEND_CARD.value)
)
async def back_from_payment_extend_card_callback(
    callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - profile.back_from_payment_extend_card_callback"
    )

    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_payment_option_text(int(data["price"]), user.balance),
        reply_markup=get_payment_options_keyboard(
            duration=int(data["duration"]),
            price=int(data["price"]),
            country=data["country"],
            order_id=data["order_id"],
            extend=True,
        ),
    )

    await callback.answer()


@profile_router.callback_query(
    BackFromPaymentCallbackFactory.filter(
        F.purpose == PaymentPurpose.EXTEND_ADD_MONEY.value
    )
)
async def back_from_payment_extend_add_money_callback(
    callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - profile.back_from_payment_extend_add_money_callback"
    )

    data = await check_not_payed(callback, callback_data)
    user = get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=get_not_enough_money_text(int(data["price"]) - user.balance),
        reply_markup=get_balance_add_money_keyboard(
            duration=int(data["duration"]),
            price=int(data["price"]),
            country=data["country"],
            add=int(data["price"]) - user.balance,
            order_id=int(data["order_id"]),
        ),
    )

    await callback.answer()


# --- profile info ---


@profile_router.callback_query(ProfileCallbackFactory.filter())
async def profile_order_info_callback(
    callback: CallbackQuery, callback_data: ProfileCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.profile_order_info_callback")

    await callback.message.edit_text(
        text=get_profile_add_money_text(),
        reply_markup=get_add_money_keyboard(),
    )
    await callback.answer()


@profile_router.callback_query(ProfileAddMoneyCallbackFactory.filter(F.back == True))
async def add_money_back_callback(
    callback: CallbackQuery, callback_data: ProfileAddMoneyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.add_money_back_callback")

    id = callback.from_user.id

    await callback.message.edit_text(
        text=get_profile_text(id), reply_markup=get_profile_keyboard()
    )
    await callback.answer()


@profile_router.callback_query(ProfileAddMoneyCallbackFactory.filter(F.back == False))
async def add_money_callback(
    callback: CallbackQuery, callback_data: ProfileAddMoneyCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.add_money_callback")

    await buy_handle(
        callback,
        callback_data,
        callback_data.amount,
        purpose=PaymentPurpose.ADD_MONEY,
        title="Пополнение баланса",
        description=f"Баланс - аккаунт ID: {callback.from_user.id}",
    )


@profile_router.callback_query(
    BackFromPaymentCallbackFactory.filter(F.purpose == PaymentPurpose.ADD_MONEY.value)
)
async def back_from_payment_add_money_callback(
    callback: CallbackQuery, callback_data: BackFromPaymentCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - profile.back_from_payment_add_money_callback"
    )

    await check_not_payed(callback, callback_data)

    await callback.message.edit_text(
        text=get_profile_add_money_text(),
        reply_markup=get_add_money_keyboard(),
    )
    await callback.answer()


# --- notifications callbacks ---


@profile_router.callback_query(OrderExpiringCallbackFactory.filter())
async def profile_extend_expiring_key_callback(
    callback: CallbackQuery, callback_data: OrderExpiringCallbackFactory
):
    bot_logger.info(
        f"Callback: '{callback.id}' - profile.profile_extend_expiring_key_callback"
    )

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


@profile_router.callback_query(InfoVPNNotificationCallbackFactory.filter())
async def get_review_on_vpn_callback(
    callback: CallbackQuery, callback_data: InfoVPNNotificationCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.get_review_on_vpn_callback")

    text = callback_data.text
    if text == forgot_buy:
        await callback.message.edit_text(
            text=forgot_buy_text(), reply_markup=get_buy_vpn_from_notify_keyboard()
        )
    elif text == bad_price:
        update_user(
            callback.from_user.id,
            {
                "sale": 30,
                "sale_expiration": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=30),
            },
        )
        await callback.message.edit_text(
            text=bad_price_text(), reply_markup=get_buy_vpn_from_notify_keyboard()
        )
    else:
        await callback.message.edit_text(text=thanks_for_review_text())

    update_user(callback.from_user.id, {"review": " ".join(text.split(" ")[1:])})


@profile_router.callback_query(BuyVPNFromNotificationCallbackFactory.filter())
async def buy_vpn_from_notify_callback(
    callback: CallbackQuery, callback_data: BuyVPNFromNotificationCallbackFactory
):
    bot_logger.info(f"Callback: '{callback.id}' - profile.buy_vpn_from_notify_callback")

    await callback.message.edit_text(
        text=get_buy_vpn_text(),
        reply_markup=get_buy_vpn_keyboard(user_id=callback.from_user.id, extend=False),
    )
