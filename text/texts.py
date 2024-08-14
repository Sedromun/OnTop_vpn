import datetime

from config import CONNECT_INSTR_URL, MIN_ADD_AMOUNT
from database.controllers.user import get_user
from utils.common import datetime_format
from utils.country import COUNTRIES
from utils.payment import get_order_perm_key


def get_greeting_text():
    return (
        "👋 Добро пожаловать в бота <b>OnTop VPN</b>!\n\n"
        "⚡️ Здесь ты можешь приобрести премиум подписку, получая беспрерывный доступ к высокоскоростному VPN"
        " по лояльной цене!\n\n"
        "🏆 <b>Наши привелегии</b>:\n"
        "• <i>Обход всех блокировок и ограничений (включая YouTube)</i>\n"
        "• <i>Быстрая и удобная смена стран</i>\n"
        "• <i>Конфиденциальность, приватность и анонимность</i>\n"
        "• <i>Трафик популярных российских сайтов идёт напрямую, a не через сервер</i>\n"
        "• <i>Побеждает китайскийе фаерволы</i>\n"
        "• <i>Совместимость с Torrent, Tor и многое другое :)</i>"
    )


def get_incorrect_command():
    return "Такой команды нет"


def get_information_text():
    return "Здесь вы можете найти доступные для подключения страны, наш канал и отзывы пользователей"


def get_profile_text(id: int):
    user = get_user(id)
    return f"🏦Ваш баланс: {str(user.balance)} ₽\n\n" f"🙋🏻‍♂️ID: {str(id)}\n"


def get_buy_vpn_text():
    return "🛡️<b>Выберите тариф</b>:"


def get_payment_option_text(amount: int, balance: int):
    return f"💸К оплате {amount}₽\n\n🏦На балансе {balance}₽\n\n<b>Выберите тип оплаты:</b>"


def get_success_created_key_text(key: str):
    return (
        f"🎉 <b>Благодарим за покупку!</b>\n\n<a href='{CONNECT_INSTR_URL}'>⚙️ Инструкция по "
        f"подключению</a>\n\n"
    )


def get_payment_choose_country_text():
    return "Выберите страну для <b>VPN</b>\n<i>(Её можно будет изменить)</i>"


def get_not_enough_money_text(add: int):
    return (
        "На балансе недостаточно средств\n<i>Не достаточно: " + str(add)
        + "₽</i>\n\n<b>Выберите сумму для пополнения</b>"
        + ("\nминимальная сумма пополнения 90₽" if add < MIN_ADD_AMOUNT else "")
    )


def get_pay_text():
    return "Для оплаты нажмите на кнопку"


def get_key_data(order):
    return (
        f"Страна: {order.country} {COUNTRIES[order.country]}\n\n"
        f"Дата истечения: {order.expiration_date.strftime(datetime_format)}\n"
        f"(осталось {(order.expiration_date - datetime.datetime.now(datetime.timezone.utc)).days} дней)\n\n"
        f"Ключ:\n<code>{get_order_perm_key(order.id)}</code>"
    )


def get_referral_bought(amount: int):
    return (f"🎉 Поздравляем, по вашей реферальной ссылке была совершена покупка - вам начислена награда: {amount}₽"
            f" - уже зачислены на ваш баланс")


def order_expired_text(order_id: int):
    return (f"Время действия вашего VPN ключа {order_id} истекло.\n\nСпасибо что выбрали нас!\n\n"
            f"Не забудьте оформить новый ключ!")


def order_going_to_expired_text(order_id: int, time: str):
    return (f"Время действия вашего VPN ключа {order_id} истекает через {time}.\n\nНе забудьте продлить время его"
            f" действия")