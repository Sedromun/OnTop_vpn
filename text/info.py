from config import SUPPORT_TAG, RECALLS_TGC_TAG
from utils.country import COUNTRIES


def get_countries_text():
    countries_text = ''
    for country, flag in COUNTRIES.items():
        countries_text += f'{country} {flag}\n'
    return "Мы поддерживаем сервера в этих странах:\n" + countries_text


def get_tech_support_text():
    return "Если у вас возникли какие-то проблемы можете обратиться в поддержку:\n" + SUPPORT_TAG


def get_recalls_text():
    return "Вы можете посмотреть отзывы в канале:\n" + RECALLS_TGC_TAG