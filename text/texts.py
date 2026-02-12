import datetime

from config import MIN_ADD_AMOUNT, INSTR_URL
from database.controllers.user import get_user, register_user
from utils.common import datetime_format
from utils.country import COUNTRIES
from utils.payment import get_order_vless_key


def get_greeting_text():
    return (
        "🎉 Привет! Ты в <b>Clique VPN</b> — где доступ к любимым сервисам"
        " никогда не ограничен.\n\n"
        "Для навигации и подключения воспользуйся клавиатурой:\n\n"
        "🛒 <b>Купить подписку</b> - доступные тарифы и скидки\n\n"
        "👫 <b>Реферальная программа</b> - приглашай и зарабатывай\n\n"
        "⚙️ <b>Настройки</b> - информация о ключах и смене страны\n\n"
        f"А инструкцию по подключению ты найдешь <a href='{INSTR_URL}'>здесь</a>"
    )


def get_present_greeting_text():
    return (
        "❤ Привет! Твой друг подарил тебе подписку на наш сервис. Она уже активирована, информацию по подключению в сообщении ниже\n\n"
        "Для навигации и подключения воспользуйся клавиатурой:\n\n"
        "🛒 <b>Купить подписку</b> - доступные тарифы и скидки\n\n"
        "👫 <b>Реферальная программа</b> - приглашай и зарабатывай\n\n"
        "⚙️ <b>Настройки</b> - информация о ключах и смене страны\n\n"
        f"А инструкцию по подключению ты найдешь <a href='{INSTR_URL}'>здесь</a>"
    )


def get_incorrect_command():
    return "Такой команды нет"


def get_information_text():
    return "⚙️ Здесь ты можешь изменить настройки ключей и посмотреть свой баланс"


def get_profile_text(id: int):
    user = get_user(id)
    if user is None:
        register_user(id)
    return (
        f"📂 <b>Твой профиль:</b> \n\n"
        f"💰 Баланс: {str(user.balance)} ₽\n\n"
        f"🆔 ID: {str(id)}"
    )


def get_buy_vpn_text():
    return "🎯️ <b>Выбери тип подписки</b>:"


def get_payment_option_text(amount: int, balance: int):
    return (
        f"💸 К оплате {amount}₽\n\n🏦На балансе {balance}₽\n\n<b>Выбери тип оплаты:</b>"
    )


def get_success_created_key_text():
    return "🎉 <b>Благодарим за покупку!</b>\n\n"


def get_success_created_present_text(link: str):
    return (f"🎉 <b>Поздравляем с покупкой!</b>\n\nДля активации подарка - "
            f"отправьте ссылку получателю подарка <i>(сами не открывайте ссылку - она одноразовая)</i>:\n\n <code>{link}</code>")


def get_payment_choose_country_text():
    return "🌍 Выбери <b>страну</b> для <b>VPN</b>\n<i>(Её можно будет изменить)</i>"

def get_person_option_buy_text():
    return "Для кого ты хочешь оформить подписку?"


def get_not_enough_money_text(add: int):
    return (
            "❌ <b>На балансе недостаточно средств</b>\n\nНе достаточно: "
            + str(add)
            + "₽\n\n<i>Выбери сумму для пополнения</i>"
            + (
                f"\nминимальная сумма пополнения {MIN_ADD_AMOUNT}₽"
                if add < MIN_ADD_AMOUNT
                else ""
            )
    )


def get_key_data(order):
    return (
            f"Страна: {order.country} {COUNTRIES[order.country]}\n\n"
            f"Дата истечения ключа"
            + (
                " и продления подписки"
                if (order.payment_id != "" and order.payment_id is not None)
                else ""
            )
            + f": {(order.expiration_date.astimezone(datetime.timezone.utc) + datetime.timedelta(hours=3)).strftime(datetime_format)}\n"
              f"(осталось {get_left_time(order.expiration_date.astimezone(datetime.timezone.utc))})\n\n"
              f"Ключи (нажми, чтобы скопировать):\n\n<i>VLESS:</i>\n<code>{get_order_vless_key(order.id)}</code>"
            + "\n\n<i>Советуем выбирать VLESS (он стабильнее и быстрее)\n<b>Подробности по установке в инструкции</b></i> 👇"
    )


def get_left_time(expiration_date: datetime.datetime):
    current = datetime.datetime.now(datetime.timezone.utc)
    if (expiration_date - current).days > 0:
        return str((expiration_date - current).days) + " дней"
    elif (expiration_date - current).seconds // 3600 > 0:
        return str((expiration_date - current).seconds // 3600) + " часов"
    else:
        return str((expiration_date - current).seconds // 60) + " минут"


def get_payment_text():
    return "🫰 Оплати по ссылке"


def get_old_user_message_start_text():
    return (
        "❤️ Привет! Спасибо, что доверяешь нам!\n\n"
        "В этом боте мы немного изменили интерфейс, чтобы тебе было удобнее пользоваться нашим сервисом.\n\n"
        "Кроме того, для всех старых пользователей мы продлили подписку на 2 недели!\n"
        "Чтобы продление сработало, тебе нужно обновить свои ключи. "
        "Для этого перейди в <i>“Настройки”</i> > <i>“Мои ключи”</i>,"
        " скопируй ключ и вставь его в приложение <b>Outline</b>.\n\n"
        "Для навигации и подключения воспользуйся клавиатурой:\n\n"
        "🛒 <b>Купить подписку</b> - доступные тарифы и скидки\n\n"
        "👫 <b>Реферальная программа</b> - приглашай и зарабатывай\n\n"
        "⚙️ <b>Настройки</b> -  информация о ключах и смене страны\n\n"
    )
