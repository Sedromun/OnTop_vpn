from utils.buy_options import get_option_price, get_option_sale_price
from utils.country import COUNTRIES

buy = "🛒 Купить подписку"
settings = "⚙️ Настройки"
profile = "👤 Профиль"
tech_support = "👨‍🔧 Поддержка"
recalls = "📕 Канал"
top_up_balance = "💸 Пополнить баланс"
balance = "💰 Баланс"
card = "💳 Карта"
change_country = "🌎 Изменить страну"
back = "⬅️ Назад"
extend_key = "🔑 Продлить подписку"
referral_program = "👫 Реферальная программа"
all_instr = "📖 Инструкция"
pay = "Оплатить"
off_auto = "Отключить автопродление"
my_keys = "🔑 Мои ключи"
bad_price = "💸 Не устраивает цена"
bad_quality = "🔑 Не устраивает качество"
another_service = "📡 Нашел другой сервис"
dont_vpn = "❌ Не пользуюсь VPN"
forgot_buy = "📌 Забыл оформить"


def get_order_short_text(order_id: int, country: str):
    return f"Ключ №{order_id} - {country} {COUNTRIES[country]}"


def get_buy_option_text(option, user_id, order_id):
    return (
        "⏳ " + option + " | " + str(get_option_price(option, user_id, order_id)) + "₽"
    )


def get_buy_option_sale_text(option, sale):
    return (
        "🔥 "
        + option
        + " | "
        + str(get_option_sale_price(option, sale))
        + "₽ (-"
        + str(sale)
        + "%)"
    )


def get_country_text(value: str, flag: str):
    return value + " " + flag
