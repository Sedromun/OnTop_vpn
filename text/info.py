import datetime

from config import PERCENT_REFERRAL, WELCOME_PRESENT
from text.keyboard_text import buy
from utils.common import datetime_format, get_referral_link
from utils.country import COUNTRIES


def get_referral_program_text(user_id: int):
    return (
        "<b>💸 Зарабатывай с нами!</b>\n\n"
        f"Приглашай друзей в «<b>Clique VPN</b>» и получай <b>{PERCENT_REFERRAL}%</b>"
        f" с каждой их покупки на свой баланс! "
        f"А новый пользователь получает "
        f"<b>{WELCOME_PRESENT}₽</b> в подарок при первом подключении!\n\n"
        f"<i>P.S.</i> Если пять твоих друзей оформят подписку на месяц,"
        f" то ты сможешь пользоваться нашим сервисом <b>бесплатно</b>\n\n"
        f"<b>Твоя реферальная ссылка:</b>\n"
        f"<code>{get_referral_link(user_id)}</code>"
    )


def get_no_orders_text():
    return f"Ты еще не оформил ни один ключ, воспользуйся кнопкой \n{buy}"


def expiration_date_text(order):
    return (f"Ключ №{order.id} {COUNTRIES[order.country]}\n\nДата истечения" +
            (" и продления подписки" if (order.payment_id != "" and order.payment_id is not None) else "") +
            f": {(order.expiration_date.astimezone(datetime.timezone.utc) + datetime.timedelta(hours=3)).strftime(datetime_format)}\n\n")


def auto_off_text(order_id):
    return f"✅ <b>Автопродление для ключа №{order_id} - отключено</b>\n\n"


def get_my_keys_text():
    return "🔑 <b>Твои ключи</b> - выбери ключ, чтобы изменить его"
