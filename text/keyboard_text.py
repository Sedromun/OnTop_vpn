from config import ONE_DAY_SALE
from utils.buy_options import get_option_price, get_option_sale_price
from utils.country import COUNTRIES

buy = "🛒 Купить"
settings = "⚙️ Настройки"
profile = "👤 Профиль"
countries = "🌎 Страны"
tech_support = "👷🏻 Тех. Поддержка"
recalls = "📕 Канал"
top_up_balance = "💸 Пополнить баланс"
balance = "💰 Баланс"
card = "💳 Карта"
change_country = "🌎 Изменить страну"
back = "⬅️ Назад"
extend_key = "🔑 Продлить ключ"
connect_instr = "⚙️ Инструкция по подключению"
referral_program = "👫 Реферальная программа"
buy_instr = "⚙️ Инструкция по покупке VPN"
change_country_instr = "⚙️ Инструкция по смене страны"
all_instr = "⚙️ Инструкция"
pay = "Оплатить"
off_auto = "Отключить автопродление"


def get_order_short_text(order_id: int, country: str):
    return f"Ключ №{order_id} - {country} {COUNTRIES[country]}"


def get_buy_option_text(option):
    return "⏳ " + option + " | " + str(get_option_price(option)) + "₽"


def get_buy_option_sale_text(option):
    return "🔥 " + option + " | " + str(get_option_sale_price(option)) + "₽ (-" + str(ONE_DAY_SALE) + "%)"


def get_country_text(value: str, flag: str):
    return value + " " + flag
