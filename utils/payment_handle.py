from aiogram.types import CallbackQuery

from config import BOT_URL
from yookassa import Payment

from keyboards.buy import get_payment_to_yookassa_keyboard
from text.texts import get_payment_text


async def buy_handle(
        callback: CallbackQuery,
        callback_data,
        amount: int,
        order_id: int,
        title: str,
        description: str,
        extend: bool = False,
        add_money: bool = False
):
    payment = Payment.create({
        "amount": {"value": amount, "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": BOT_URL
        },
        "capture": True,
        "description": "VPN",
        "save_payment_method": True,
        "metadata": {
            "order_id": order_id,
            "message_id": callback.message.message_id,
            "duration": callback_data.duration,
            "extend": "E" if extend else ("A" if add_money else "C")
        }
    })

    await callback.message.edit_text(
        get_payment_text(),
        reply_markup=get_payment_to_yookassa_keyboard(url=payment.confirmation)
    )
    await callback.answer()