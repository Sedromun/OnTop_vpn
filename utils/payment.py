from aiogram import types

from config import bot, PAYMENTS_PROVIDER_TOKEN


async def buy_handle(callback, callback_data, amount: int, order_id: int, extend: bool = False, add_money: bool = False):
    await bot.send_invoice(
        callback.from_user.id,
        title="Оплата",
        description="Оплата",
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=[types.LabeledPrice(label='VPN', amount=amount * 100)],
        start_parameter='top-vpn-payment-deeplink',
        payload=('E' if extend else ('A' if add_money else 'C')) + '_' + str(order_id) + '_' + str(callback_data.duration),
    )
    await callback.message.delete()
    await callback.answer()
