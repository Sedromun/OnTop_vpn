import json

from aiogram import types

from config import KEYS_URL, PAYMENTS_PROVIDER_TOKEN, bot, FERNET


async def buy_handle(
        callback,
        callback_data,
        amount: int,
        order_id: int,
        title: str,
        description: str,
        extend: bool = False,
        add_money: bool = False
):
    provider_data = {
        "receipt":
            {
                "items":
                    [{
                        "description": "VPN",
                        "quantity": "1",
                        "amount": {"value": amount, "currency": "RUB"},
                        "vat_code": 1
                    }],
            }
    }

    await bot.send_invoice(
        callback.from_user.id,
        title=title,
        description=description,
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        need_email=True,
        send_email_to_provider=True,
        provider_data=json.dumps(provider_data),
        currency="rub",
        is_flexible=False,
        prices=[types.LabeledPrice(label="VPN", amount=amount * 100)],
        start_parameter="top-vpn-payment-deeplink",
        payload=("E" if extend else ("A" if add_money else "C"))
                + "_"
                + str(order_id)
                + "_"
                + str(callback_data.duration),
    )
    await callback.message.delete()
    await callback.answer()


def get_order_perm_key(order_id: int) -> str:
    to_encrypt = str(order_id)
    order_id_enc = FERNET.encrypt(to_encrypt.encode())
    return KEYS_URL + order_id_enc.decode()
