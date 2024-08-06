from utils.buy_options import get_option_price
from utils.country import COUNTRIES

buy = "🛒 Купить"
info = "ℹ️ Информация"
profile = "👤 Профиль"
countries = "🌎 Страны"
tech_support = "👷🏻 Тех. Поддержка"
recalls = "📕 Отзывы"
top_up_balance = "💸 Пополнить баланс"
balance = "💰 Баланс"
card = "💳 Карта"
change_country = "🌎 Изменить страну"
back = "⬅️ Назад"
extend_key = "🔑 Продлить ключ"
connect_instr = "⚙️ Инструкция по подключению"


def get_order_short_text(order_id: int, country: str):
    return f"Ключ №{order_id} - {country} {COUNTRIES[country]}"


def get_buy_option_text(option):
    return "🔥 " + option + " | " + str(get_option_price(option)) + "₽"


def get_country_text(value: str, flag: str):
    return value + " " + flag
