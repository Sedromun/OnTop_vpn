from database.controllers.order import get_order
from text.texts import get_key_data
from utils.country import COUNTRIES


def get_order_info_text(order_id):
    order = get_order(order_id)
    return f"🔑 <b>Информация о ключе №{order_id}</b>:\n\n{get_key_data(order)}"


def get_order_choose_country_text(id, country):
    return (
        f"Выберите <b>страну</b> для изменения\n<b>Ключ №{id}</b>\n\n"
        f"🌎 Текущая страна: {country} {COUNTRIES[country]}\n"
    )


def get_country_changed_text(order_id: int):
    return (
        f"✅ <b>Страна успешно изменена</b>\n\n"
        f"После смены страны <b>не забудь перезапустить VPN</b> в приложении outline<\n\n" +
        get_order_info_text(order_id)
    )


def get_success_extended_key_text():
    return "🎉 <b>Ключ успешно продлен!</b>\n\n"


def get_profile_add_money_text():
    return "💸 <b>Выберите сумму для пополнения</b>:"


def get_money_added_text():
    return "🎉 <b>Счет успешно пополнен!</b>"
