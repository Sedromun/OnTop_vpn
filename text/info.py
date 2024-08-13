from config import RECALLS_TGC_TAG, WELCOME_PRESENT, PERCENT_REFERRAL
from utils.common import get_referral_link
from utils.country import COUNTRIES


def get_countries_text():
    countries_text = ""
    for country, flag in COUNTRIES.items():
        countries_text += f"{country} {flag}\n"
    return "Мы поддерживаем сервера в следующих странах:\n\n" + countries_text


def get_recalls_text():
    return "Посмотрите отзывы :\n" + RECALLS_TGC_TAG


def get_referral_program_text(user_id: int):
    return ("В рамках нашей реферальной программы\n\n⚡️ С каждого приглашенного вами пользователя,"
            f" вам на баланс будут начислены <i>{PERCENT_REFERRAL}%</i> с каждой его покупки!\n\n⚡️Приглашенному "
            f"пользователю"
            f"начислят <i>{WELCOME_PRESENT}₽</i> на баланс в качестве приветсвенного бонуса!\n\nВаша реферальная "
            f"ссылка:\n"
            f"<code>{get_referral_link(user_id)}</code>")
