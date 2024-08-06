import datetime

from database.controllers.order import get_order
from utils.country import COUNTRIES

datetime_format = '%Y-%m-%d %H:%M'


def get_order_info_text(order_id):
    order = get_order(order_id)
    return (f"Информация о ключе:\nСтрана: {order.country} {COUNTRIES[order.country]}\n"
            f"Дата истечения: {order.expiration_date.strftime(datetime_format)} "
            f"(осталось {(order.expiration_date - datetime.datetime.now(datetime.timezone.utc)).days} days)\n")


def get_order_choose_country_text(country):
    return f"Выберите страну для изменения, сейчас: {country} {COUNTRIES[country]}\n"


def get_country_changed_text(country):
    return f"Страна успешно изменена:\n {country} {COUNTRIES[country]}\n"


def get_success_extended_key_text():
    return "Ключ продлен:\n"


def get_profile_add_money_text():
    return "Выберите сумму для пополнения:"


def get_money_added_text():
    return "Денежка упала на баланс"
