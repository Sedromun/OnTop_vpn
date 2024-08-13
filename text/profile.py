from database.controllers.order import get_order
from text.texts import get_key_data
from utils.country import COUNTRIES


def get_order_info_text(order_id):
    order = get_order(order_id)
    return f"🔑 <b>Информация о ключе</b>:\n\n{get_key_data(order)}"


def get_order_choose_country_text(country):
    return f"Выберите <b>страну</b> для изменения\n\n🌎 Текущая страна: {country} {COUNTRIES[country]}\n"


def get_country_changed_text(country):
    return (f"🌎 <b>Страна успешно изменена</b>\n"
            f"<i>После смены страны не забудьте перезапустить vpn в приложении outline</i>\n"
            f" {country} {COUNTRIES[country]}\n\n")


def get_success_extended_key_text():
    return "🎉 <b>Ключ успешно продлен!</b>\n"


def get_profile_add_money_text():
    return "💸 <b>Выберите сумму для пополнения</b>:"


def get_money_added_text():
    return "🎉 Денежка упала на баланс"
