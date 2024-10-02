from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from config import BOT_URL
from yookassa import Payment

from database.controllers.user import get_user
from keyboards.buy import get_payment_to_yookassa_keyboard
from text.texts import get_payment_text


class PaymentPurpose(Enum):
    BUY_CARD = 0
    BUY_ADD_MONEY = 1
    EXTEND_CARD = 2
    EXTEND_ADD_MONEY = 3
    ADD_MONEY = 4


async def check_not_payed(callback: CallbackQuery, callback_data: CallbackData) -> dict:
    user = get_user(callback.from_user.id)
    if user is None:
        await callback.message.delete()
        return

    payment = Payment.find_one(callback_data.payment_id)

    if payment.status == "succeeded":
        try:
            await callback.message.delete()
        except Exception:
            pass
        return

    return payment.metadata


async def buy_handle(
        callback: CallbackQuery,
        callback_data: CallbackData,
        amount: int,
        title: str,
        description: str,
        purpose: PaymentPurpose,
        order_data: dict = None,
        order_id: int = -1
):
    metadata = {
            "order_id": order_id,
            "message_id": callback.message.message_id,
            "duration": callback_data.duration,
            "purpose": purpose.value
        } | (order_data if order_data is not None else {})

    payment = Payment.create({
        "amount": {"value": amount, "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": BOT_URL
        },
        "capture": True,
        "description": title + "\n" + description,
        "save_payment_method": True,
        "metadata": metadata
    })

    await callback.message.edit_text(
        get_payment_text(),
        reply_markup=get_payment_to_yookassa_keyboard(
            url=payment.confirmation['confirmation_url'],
            payment_id=payment.id,
            purpose=purpose.value
        )
    )
    await callback.answer()
