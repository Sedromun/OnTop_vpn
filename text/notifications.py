from config import INSTR_URL, ONE_DAY_SALE
from database.controllers.order import get_order
from text.keyboard_text import get_order_short_text
from text.profile import get_order_info_text
from utils.country import COUNTRIES


def new_user_notification_text():
    return (
        f"Если тебе нужна помощь по использованию бота, можешь воспользоваться <a href='{INSTR_URL}'>инструкцией</a>\n\n"
        "А чтобы уже сейчас начать пользоваться VPN, нажми кнопку <b>«Купить подписку»</b>"
    )


def sale_one_day_notification_text():
    return (
            "🔥 <i>ГОРЯЧЕЕ ПРЕДЛОЖЕНИЕ!</i>\n\n"
            "<b>Для новых пользователей действует акция - "
            + str(ONE_DAY_SALE)
            + "% на месячную подписку!</b>\n\n"
              "💸 Чтобы оформить ее нажми кнопку <b>«Купить подписку»</b>\n\n"
              "<i>P.S скидка актуальна только в течение 24 часов</i>"
    )


def auto_extended_success(order_id):
    order = get_order(order_id)
    return (
        f"✅ {get_order_short_text(order_id, order.country)} - <b>успешно продлен!</b>\n\n" +
        get_order_info_text(order_id) +
        "❤️ Спасибо, что остаешься с нами!"
    )


def auto_extended_failure(order_id):
    order = get_order(order_id)
    return (
        f"❌ Автопродление для ключа {order_id} - {order.country} {COUNTRIES[order.country]} <b>не сработало</b>,"
        f" чтобы продлить его вручную нажми на кнопку “Продлить подписку”\n\n"
        f"Для твоего удобства мы автоматически <b>продлили ключ на день.</b>"
    )


def get_referral_bought(amount: int):
    return (
        f"🎉 Поздравляем, по вашей реферальной ссылке была совершена покупка - вам начислена награда: {amount}₽"
        f" - уже зачислены на ваш баланс"
    )


def order_expired_text(order_id: int, country: str):
    return (
        f"⏰ Время действия вашего VPN ключа {order_id} - {country} {COUNTRIES[country]} <b>истекло</b>.\n\nСпасибо что выбрали нас!\n\n"
        f"Не забудьте оформить новый ключ!"
    )


def order_going_to_expired_text(order_id: int, country: str, time: str):
    return (
        f"⏰ Время действия вашего VPN ключа {order_id} - {country} {COUNTRIES[country]} <b>истекает через {time}</b>.\n\nНе забудьте продлить время его"
        f" действия"
    )
