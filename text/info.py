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
    return ("<b>💸 Зарабатывай с нами!</b>\n\n"
            f"Приглашай друзей в «OnTop VPN» и получай  <i>{PERCENT_REFERRAL}%</i>"
            f" с каждой их покупки на свой баланс! "
            f"А новый пользователь получает"
            "<i>{WELCOME_PRESENT}₽</i>  подарок при первом подключении!\n\n"
            "<b>Твоя реферальная ссылка:</b>\n"
            f"<code>{get_referral_link(user_id)}</code>")
