import datetime

from config import PERCENT_REFERRAL, WELCOME_PRESENT
from text.keyboard_text import buy
from utils.common import datetime_format, get_referral_link
from utils.country import COUNTRIES


def get_countries_text():
    countries_text = ""
    for country, flag in COUNTRIES.items():
        countries_text += f"{country} {flag}\n"
    return "Мы поддерживаем сервера в следующих странах:\n\n" + countries_text


def get_referral_program_text(user_id: int):
    return (
        "<b>💸 Зарабатывай с нами!</b>\n\n"
        f"Приглашай друзей в «Clique VPN» и получай <i>{PERCENT_REFERRAL}%</i>"
        f" с каждой их покупки на свой баланс! "
        f"А новый пользователь получает "
        f"<i>{WELCOME_PRESENT}₽</i> в подарок при первом подключении!\n\n"
        f"<b>Твоя реферальная ссылка:</b>\n"
        f"<code>{get_referral_link(user_id)}</code>"
    )


def choose_order_to_change_country():
    return "Выбери ключ в котором хотите поменять страну"


def choose_order_to_off_auto():
    return "Выбери ключ для отмены автопродления"


def choose_order_to_extend():
    return "Выбери ключ для продления"


def get_no_orders_text():
    return f"Ты еще не оформил ни один ключ, воспользуйся кнопкой \n{buy}"


def expiration_date_text(order):
    return f"Ключ №{order.id} {COUNTRIES[order.country]}\n\nДата истечения: {(order.expiration_date.astimezone(datetime.timezone.utc) + datetime.timedelta(hours=3)).strftime(datetime_format)}\n\n"


def auto_off_text(order_id):
    return f"✅ <b>Автопродление для ключа №{order_id} - отключено</b>\n\n"


def get_my_keys_text():
    return "🔑 Твои ключи - выбери ключ, чтобы изменить его"
