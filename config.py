import datetime
import os

from aiogram import Bot, Dispatcher
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import SecretStr

from outline.outline_vpn.outline_vpn import OutlineVPN
from py3xui.api.api import Api
from py3xui.async_api.async_api import AsyncApi

load_dotenv()

# -- bot --

BOT_TOKEN: SecretStr = SecretStr(os.getenv("BOT_TOKEN"))
bot = Bot(
    BOT_TOKEN.get_secret_value(), parse_mode="HTML", disable_web_page_preview=True
)
dp = Dispatcher()

# -- database --

DB_USER = str(os.getenv("DB_USER"))
DB_URL = str(os.getenv("DB_URL"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))

# -- backend --

HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))
DOMEN = str(os.getenv("DOMEN"))

# -- encrypt --

CRYPTO_KEY = str(os.getenv("CRYPTO_KEY"))
FERNET = Fernet(CRYPTO_KEY)

# -- payments --

SHOP_ID = str(os.getenv("SHOP_ID"))
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# -- links --

TECH_SUPPORT_LINK = "https://t.me/" + str(os.getenv("TECH_SUPPORT_TAG"))
RECALLS_TGC_LINK = "https://t.me/" + str(os.getenv("RECALLS_TGC_TAG"))
INSTR_URL = str(os.getenv("INSTR_URL"))
BOT_URL = str(os.getenv("BOT_URL"))
REFS_PARAM = "?start="
SECRET_START_STRING = str(os.getenv("SECRET_START_STRING"))

# -- Numeric params --

MIN_ADD_AMOUNT = 50
PERCENT_REFERRAL = 40
WELCOME_PRESENT = 50
ONE_DAY_SALE = 30
THIRD_DAY_SALE = 20
INTERVAL = 5  # mins

OLD_USER_UNTIL_DATE = datetime.datetime.strptime(
    "2024-10-13 00-00-00", "%Y-%m-%d %H-%M-%S"
)

# -- admins --

SAVVA_ADMIN = str(os.getenv("SAVVA_ADMIN"))
EVGENIY_ADMIN = str(os.getenv("EVGENIY_ADMIN"))
TECH_SUPPORT_ADMIN = str(os.getenv("TECH_SUPPORT_ADMIN"))

ADMINS = [SAVVA_ADMIN, EVGENIY_ADMIN, TECH_SUPPORT_ADMIN]

# -- outline --

SWEDEN_API_URL_1 = str(os.getenv("SWEDEN_API_URL_1"))
SWEDEN_CERT_SHA256_1 = str(os.getenv("SWEDEN_CERT_SHA256_1"))
RUSSIAN_API_URL_1 = str(os.getenv("RUSSIAN_API_URL_1"))
RUSSIAN_CERT_SHA256_1 = str(os.getenv("RUSSIAN_CERT_SHA256_1"))
RUSSIAN_API_URL_2 = str(os.getenv("RUSSIAN_API_URL_2"))
RUSSIAN_CERT_SHA256_2 = str(os.getenv("RUSSIAN_CERT_SHA256_2"))
GERMAN_API_URL_1 = str(os.getenv("GERMAN_API_URL_1"))
GERMAN_CERT_SHA256_1 = str(os.getenv("GERMAN_CERT_SHA256_1"))
GERMAN_API_URL_2 = str(os.getenv("GERMAN_API_URL_2"))
GERMAN_CERT_SHA256_2 = str(os.getenv("GERMAN_CERT_SHA256_2"))
FRANCE_API_URL_1 = str(os.getenv("FRANCE_API_URL_1"))
FRANCE_CERT_SHA256_1 = str(os.getenv("FRANCE_CERT_SHA256_1"))
GB_API_URL_1 = str(os.getenv("GB_API_URL_1"))
GB_CERT_SHA256_1 = str(os.getenv("GB_CERT_SHA256_1"))
USA_API_URL_1 = str(os.getenv("USA_API_URL_1"))
USA_CERT_SHA256_1 = str(os.getenv("USA_CERT_SHA256_1"))
LATVIA_API_URL_1 = str(os.getenv("LATVIA_API_URL_1"))
LATVIA_CERT_SHA256_1 = str(os.getenv("LATVIA_CERT_SHA256_1"))
ESTONIA_API_URL_1 = str(os.getenv("ESTONIA_API_URL_1"))
ESTONIA_CERT_SHA256_1 = str(os.getenv("ESTONIA_CERT_SHA256_1"))
NETHERLAND_API_URL_1 = str(os.getenv("NETHERLAND_API_URL_1"))
NETHERLAND_CERT_SHA256_1 = str(os.getenv("NETHERLAND_CERT_SHA256_1"))
FINLAND_API_URL_1 = str(os.getenv("FINLAND_API_URL_1"))
FINLAND_CERT_SHA256_1 = str(os.getenv("FINLAND_CERT_SHA256_1"))
AUSTRIA_API_URL_1 = str(os.getenv("AUSTRIA_API_URL_1"))
AUSTRIA_CERT_SHA256_1 = str(os.getenv("AUSTRIA_CERT_SHA256_1"))

outline_client = {
    10: OutlineVPN(api_url=RUSSIAN_API_URL_1, cert_sha256=RUSSIAN_CERT_SHA256_1),
    11: OutlineVPN(api_url=RUSSIAN_API_URL_2, cert_sha256=RUSSIAN_CERT_SHA256_2),
    20: OutlineVPN(api_url=SWEDEN_API_URL_1, cert_sha256=SWEDEN_CERT_SHA256_1),
    30: OutlineVPN(api_url=GERMAN_API_URL_1, cert_sha256=GERMAN_CERT_SHA256_1),
    31: OutlineVPN(api_url=GERMAN_API_URL_2, cert_sha256=GERMAN_CERT_SHA256_2),
    40: OutlineVPN(api_url=FRANCE_API_URL_1, cert_sha256=FRANCE_CERT_SHA256_1),
    50: OutlineVPN(api_url=GB_API_URL_1, cert_sha256=GB_CERT_SHA256_1),
    60: OutlineVPN(api_url=USA_API_URL_1, cert_sha256=USA_CERT_SHA256_1),
    70: OutlineVPN(api_url=LATVIA_API_URL_1, cert_sha256=LATVIA_CERT_SHA256_1),
    80: OutlineVPN(api_url=NETHERLAND_API_URL_1, cert_sha256=NETHERLAND_CERT_SHA256_1),
    90: OutlineVPN(api_url=FINLAND_API_URL_1, cert_sha256=FINLAND_CERT_SHA256_1),
    100: OutlineVPN(api_url=ESTONIA_API_URL_1, cert_sha256=ESTONIA_CERT_SHA256_1),
    110: OutlineVPN(api_url=AUSTRIA_API_URL_1, cert_sha256=AUSTRIA_CERT_SHA256_1),
}

VLESS_URI = str(os.getenv("VLESS_URI"))
VLESS_PORT = str(os.getenv("VLESS_PORT"))
VLESS_USERNAME = str(os.getenv("VLESS_USERNAME"))
VLESS_PASSWORD = str(os.getenv("VLESS_PASSWORD"))

vless_server_ip = {
    81: str(os.getenv("NETHERLANDS_2_IP")),
    91: str(os.getenv("FINLAND_2_IP")),
}

vless_client = {
    81: AsyncApi(f"http://{vless_server_ip[81]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    91: AsyncApi(f"http://{vless_server_ip[91]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
}

servers_countries = {
    10: "Россия",
    11: "Россия",
    20: "Швеция",
    30: "Германия",
    31: "Германия",
    40: "Франция",
    50: "Великобритания",
    60: "США",
    70: "Латвия",
    80: "Нидерланды",
    81: "Нидерланды",
    90: "Финляндия",
    91: "Финляндия",
    100: "Эстония",
    110: "Австрия",
}

servers_countries_in_email = {
    10: "Russia-1",
    11: "Russia-2",
    20: "Sweden-1",
    30: "Germany-1",
    31: "Germany-2",
    40: "France-1",
    50: "Great-Britain-1",
    60: "USA-1",
    70: "Lithuania-1",
    80: "Netherlands-1",
    81: "Netherlands-2",
    90: "Finland-1",
    91: "Finland-2",
    100: "Estonia-1",
    110: "Austria-1",
}

parameters = {
    10: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    11: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    20: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    30: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    31: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    40: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    50: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    60: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    70: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    80: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    81: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ERx8b7RTpk6DQ8IfQxgbsOOXK-rkac0V5dZhGv_99mI",
        "fp": "chrome",
        "sni": "yahoo.com",
        "sid": "1c",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    90: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    91: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ZQ6vH7Xr22l-Xf0Dp3C1mcHXhWAa8ZhY6r4rAkiIBAA",
        "fp": "chrome",
        "sni": "yahoo.com",
        "sid": "46",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    100: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    110: {
        "type": "tcp",
        "security": "reality",
        "pbk": "",
        "fp": "chrome",
        "sni": "",
        "sid": "",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
}

efficiency = {
    10: 1,
    11: 1,
    20: 1,
    30: 2,
    31: 1,
    40: 1,
    50: 1,
    60: 1,
    70: 1,
    80: 1,
    90: 1,
    100: 1,
    110: 1,
}

country_to_server_ids = {
    "Россия": [10, 11],
    "Швеция": [20],
    "Германия": [30, 31],
    "Франция": [40],
    "Великобритания": [50],
    "США": [60],
    "Латвия": [70],
    "Нидерланды": [80],
    "Финляндия": [90],
    "Эстония": [100],
    "Австрия": [110],
}

SSCONF = "ssconf"
KEYS_URL = SSCONF + "://" + DOMEN + "/keys" + "/"
VLESS_URL = "https://" + DOMEN + "/vless/"
VLESS_INBOUND_ID = 1

"""
vless://a11c8748-3882-49d1-a2f6-e183419c4f52@185.156.108.92:443?type=tcp&security=reality&pbk=ZQ6vH7Xr22l-Xf0Dp3C1mcHXhWAa8ZhY6r4rAkiIBAA&fp=chrome&sni=yahoo.com&sid=46&spx=%2F&flow=xtls-rprx-vision#clique-vpn-Finland-2-1

"""

