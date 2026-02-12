import datetime
import os

from aiogram import Bot, Dispatcher
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import SecretStr
from aiogram.client.bot import DefaultBotProperties

from py3xui.api.api import Api
from py3xui.async_api.async_api import AsyncApi

load_dotenv()

# -- bot --

BOT_TOKEN: SecretStr = SecretStr(os.getenv("BOT_TOKEN"))
bot = Bot(
    BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True)
)
dp = Dispatcher()

ONTOP_BOT_TOKEN: SecretStr = SecretStr(os.getenv("ONTOP_BOT_TOKEN"))
ontop_bot = Bot(
    ONTOP_BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True)
)
ontop_dp = Dispatcher()

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
LENDING_URL = "website"

SPECIAL_URLS = {
    'website': 'from lending',
    'instagram': 'from instagram'
}

# -- Numeric params --

MIN_ADD_AMOUNT = 50
PERCENT_REFERRAL = 20
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


VLESS_URI = str(os.getenv("VLESS_URI"))
VLESS_PORT = str(os.getenv("VLESS_PORT"))
VLESS_USERNAME = str(os.getenv("VLESS_USERNAME"))
VLESS_PASSWORD = str(os.getenv("VLESS_PASSWORD"))

vless_server_ip = {
    11: str(os.getenv("RUSSIA_1_IP")),
    31: str(os.getenv("GERMANY_1_IP")),
    70: str(os.getenv("LATVIA_1_IP")),
    81: str(os.getenv("NETHERLANDS_1_IP")),
    91: str(os.getenv("FINLAND_1_IP")),
    110: str(os.getenv("AUSTRIA_1_IP")),
    # 50: str(os.getenv("UK_1_IP")),
    60: str(os.getenv("USA_1_IP")),
    40: str(os.getenv("FRANCE_1_IP")),
    120: str(os.getenv("TURKEY_1_IP")),
    130: str(os.getenv("HONGKONG_1_IP")),
}

vless_client = {
    11: AsyncApi(f"http://{vless_server_ip[11]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    31: AsyncApi(f"http://{vless_server_ip[31]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    70: AsyncApi(f"http://{vless_server_ip[70]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    81: AsyncApi(f"http://{vless_server_ip[81]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    91: AsyncApi(f"http://{vless_server_ip[91]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    110: AsyncApi(f"http://{vless_server_ip[110]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    # 50: AsyncApi(f"http://{vless_server_ip[50]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    60: AsyncApi(f"http://{vless_server_ip[60]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    40: AsyncApi(f"http://{vless_server_ip[40]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    120: AsyncApi(f"http://{vless_server_ip[120]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
    130: AsyncApi(f"http://{vless_server_ip[130]}:{VLESS_PORT}{VLESS_URI}", VLESS_USERNAME, VLESS_PASSWORD),
}

servers_countries = {
    11: "Россия",
    31: "Германия",
    70: "Латвия",
    81: "Нидерланды",
    91: "Финляндия",
    110: "Австрия",
    # 50: "Великобритания",
    60: "США",
    40: "Франция",
    120: "Турция",
    130: "Гонконг",
}

servers_countries_in_email = {
    11: "Russia",
    31: "Germany",
    70: "Lithuania",
    81: "Netherlands",
    91: "Finland",
    110: "Austria",
    # 50: "Great-Britain",
    60: "USA",
    40: "France",
    120: "Turkey",
    130: "Hong-Kong",
}

parameters = {
    11: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ylmv9z-jJTsoELWHiavAEKTq7t1oRkIAilDVC37CYAI",
        "fp": "random",
        "sni": "russia.clique-vpn.ru",
        "sid": "4b1070630806a0",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    31: {
        "type": "tcp",
        "security": "reality",
        "pbk": "fZ8gm_Tr8VPUg4hNHFpIqYkqv0yUcWJXaf0XttO2kSo",
        "fp": "radnom",
        "sni": "germany.clique-vpn.ru",
        "sid": "83c7614c9a8cda",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    70: {
        "type": "tcp",
        "security": "reality",
        "pbk": "t126zKUpND4cYe_ysrbJplY-r2_WHs_95HWLw4C79zY",
        "fp": "random",
        "sni": "latvia.clique-vpn.ru",
        "sid": "b163e86ba3f3",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    81: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ERx8b7RTpk6DQ8IfQxgbsOOXK-rkac0V5dZhGv_99mI",
        "fp": "random",
        "sni": "netherlands.clique-vpn.ru",
        "sid": "1c",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    91: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ZQ6vH7Xr22l-Xf0Dp3C1mcHXhWAa8ZhY6r4rAkiIBAA",
        "fp": "random",
        "sni": "finland.clique-vpn.ru",
        "sid": "46",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    110: {
        "type": "tcp",
        "security": "reality",
        "pbk": "ey3QB9txQgf1EYIwnrCbZbsLy0a-YVAKHUQ7fZGuLmw",
        "fp": "random",
        "sni": "austria.clique-vpn.ru",
        "sid": "e909798f64bd",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    # 50: {
    #     "type": "tcp",
    #     "security": "reality",
    #     "pbk": "C8J4nK_U-MPhlHXieNjgi07SE3sro_Np5fT0tAignUI",
    #     "fp": "random",
    #     "sni": "www.apple.com",
    #     "sid": "25ce",
    #     "spx": "%2F",
    #     "flow": "xtls-rprx-vision"
    # },
    60: {
        "type": "tcp",
        "security": "reality",
        "pbk": "C8J4nK_U-MPhlHXieNjgi07SE3sro_Np5fT0tAignUI",
        "fp": "random",
        "sni": "www.apple.com",
        "sid": "25ce",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    40: {
        "type": "tcp",
        "security": "reality",
        "pbk": "1b302fqA4dEJX-gw5iHNq7twgXM3nRAnkEMyT80nJCg",
        "fp": "random",
        "sni": "www.yandex.com",
        "sid": "e3b346af",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    120: {
        "type": "tcp",
        "security": "reality",
        "pbk": "6knpCNBHicI-jW-0PXAy18RVkFJv3Ies3OEhMYikFDU",
        "fp": "random",
        "sni": "www.vk.com",
        "sid": "a7d8216819",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    130: {
        "type": "tcp",
        "security": "reality",
        "pbk": "E1AAVc6eZDpW69olGjPxK89-NB2enVox5w5oA8YHLCM",
        "fp": "random",
        "sni": "www.yandex.com",
        "sid": "b33d72af0f",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
}

vless_inbound_id = {
    11: 1,
    31: 1,
    70: 1,
    81: 1,
    91: 1,
    110: 1,
    # 50: 1,
    60: 1,
    40: 1,
    120: 1,
    130: 1,
}


SSCONF = "ssconf"
KEYS_URL = SSCONF + "://" + DOMEN + "/keys" + "/"
VLESS_URL = "https://" + DOMEN + "/vless/"
