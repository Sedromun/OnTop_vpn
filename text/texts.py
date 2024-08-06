from config import MIN_ADD_AMOUNT
from database.controllers.user import get_user


def get_greeting_text():
    return ("👋 Добро пожаловать в бота OnTop VPN!\n\n"
            "⚡️ Здесь ты можешь приобрести премиум подписку, получая беспрерывный доступ к высокоскоростному VPN"
            " по лояльной цене!\n\n"
            "🏆 Наши привелегии:\n"
            "✅ Обход всех блокировок и ограничений (также YouTube)\n"
            "✅ Быстрая и удобная смена страны\n"
            "✅ Конфиденциальность, приватность и анонимность\n"
            "✅ Трафик популярных российских сайтов идёт напрямую, a не через сервер\n"
            "✅ Побеждает китайскийе фаерволы\n"
            "✅ Совместимость с Torrent, Tor и многое другое :)\n")


def get_incorrect_command():
    return "Такой команды нет"


def get_information_text():
    return "Можете посмотреть информацию о нашем боте"


def get_profile_text(id: int):
    user = get_user(id)
    return (f"🏦Ваш баланс: {str(user.balance)} ₽\n"
            f"🙋🏻‍♂️ID: {str(id)}\n")


def get_buy_vpn_text():
    return "📕Выбор тарифа:"


def get_payment_option_text():
    return "Выберите тип оплаты"


def get_success_created_key_text(key: str):
    return "Ключ создан:\n" + key


def get_payment_choose_country_text():
    return "Выберите страну в которой будет vpn (её можно будет изменить)"


def get_not_enough_money_text(add: int):
    return ("На балансе недостаточно средств, не хватает: " + str(add) + "\nВведите сумму для пополнения" +
            ("\nминимальная сумма пополнения 90 руб" if add < MIN_ADD_AMOUNT else ""))


def get_pay_text():
    return "Для оплаты нажмите на кнопку"

