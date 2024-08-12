from config import RECALLS_TGC_TAG, SUPPORT_TAG
from utils.country import COUNTRIES


def get_countries_text():
    countries_text = ""
    for country, flag in COUNTRIES.items():
        countries_text += f"{country} {flag}\n"
    return "Мы поддерживаем сервера в следующих странах:\n\n" + countries_text


def get_tech_support_text():
    return (
        "Если у вас возникли какие-то проблемы или вопросы - пишите нам!\n\n"
        + SUPPORT_TAG
    )


def get_recalls_text():
    return "Посмотрите отзывы :\n" + RECALLS_TGC_TAG
