from enum import Enum

BuyOptions = [
    "1 неделя",
    "1 месяц",
    "3 месяца",
    "6 месяцев",
    "1 год"
]

Prices = {
    "1 неделя": 90,
    "1 месяц": 169,
    "3 месяца": 459,
    "6 месяцев": 869,
    "1 год": 1499
}


def get_option_price(option: str):
    return Prices[option]


LiteralDuration = {
    "неделя": 7,
    "месяц": 30,
    "месяца": 30,
    "месяцев": 30,
    "год": 365
}


def get_option_duration(option: str) -> int:
    num, literal = option.split(" ")
    return int(num) * LiteralDuration[literal]
