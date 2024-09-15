from config import ONE_DAY_SALE

BuyOptions = ["1 неделя", "1 месяц", "3 месяца", "6 месяцев", "1 год"]

ONE_DAY = "1 день"

Prices = {
    ONE_DAY: 0,
    "1 неделя": 90,
    "1 месяц": 169,
    "3 месяца": 459,
    "6 месяцев": 869,
    "1 год": 1499,
}


def get_option_price(option: str):
    return Prices[option]


def get_option_sale_price(option: str):
    return Prices[option] - Prices[option] * ONE_DAY_SALE // 100


LiteralDuration = {"день": 1, "неделя": 7, "месяц": 30, "месяца": 30, "месяцев": 30, "год": 365}


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
