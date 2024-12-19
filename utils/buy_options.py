import datetime

from config import OLD_USER_UNTIL_DATE
from database.controllers.order import get_order
from database.controllers.user import get_user

BuyOptions = ["1 неделя", "1 месяц", "3 месяца", "6 месяцев", "1 год"]

THREE_DAYS = "3 дня"

OLD_PRICES = {
    THREE_DAYS: 0,
    "1 неделя": 90,
    "1 месяц": 169,
    "3 месяца": 459,
    "6 месяцев": 869,
    "1 год": 1499,
}

NEW_PRICES = {
    THREE_DAYS: 0,
    "1 неделя": 99,
    "1 месяц": 189,
    "3 месяца": 499,
    "6 месяцев": 899,
    "1 год": 1599,
}


def get_option_price(option: str, user_id: int, order_id: int) -> int:
    if user_id == -1:
        order = get_order(order_id)
        if order is not None:
            user_id = order.user_id

    user = get_user(user_id)

    is_old_prices = False

    if user is not None:
        if user.created_time.astimezone(
            datetime.timezone.utc
        ) < OLD_USER_UNTIL_DATE.astimezone(datetime.timezone.utc):
            is_old_prices = True

    return OLD_PRICES[option] if is_old_prices else NEW_PRICES[option]


def get_option_sale_price(option: str, sale):
    return NEW_PRICES[option] - NEW_PRICES[option] * sale // 100


LiteralDuration = {
    "дня": 1,
    "неделя": 7,
    "месяц": 30,
    "месяца": 30,
    "месяцев": 30,
    "год": 365,
}


def get_option_duration(option: str) -> int:
    num, literal = option.split(" ")
    return int(num) * LiteralDuration[literal]


def duration_to_str(duration: int) -> str:
    if duration // 365 > 0:
        return "1 год"
    if duration // 30 > 0:
        if duration // 30 == 1:
            return "1 месяц"
        if duration // 30 == 3:
            return "3 месяца"
        if duration // 30 == 6:
            return "6 месяцев"
        return str(duration // 30) + " месяцев"
    if duration // 7 == 1:
        return "1 неделя"
    return str(duration) + " дней"
