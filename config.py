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
VLESS_PROXY = os.getenv("VLESS_PROXY")

vless_server_ip = {
    11: str(os.getenv("RUSSIA_1_IP")),
    31: str(os.getenv("GERMANY_1_IP")),
    70: str(os.getenv("LATVIA_1_IP")),
    81: str(os.getenv("NETHERLANDS_1_IP")),
    91: str(os.getenv("FINLAND_1_IP")),
    110: str(os.getenv("AUSTRIA_1_IP")),
    50: str(os.getenv("UK_1_IP")),
    60: str(os.getenv("USA_1_IP")),
    40: str(os.getenv("FRANCE_1_IP")),
    120: str(os.getenv("TURKEY_1_IP")),
    130: str(os.getenv("HONGKONG_1_IP")),
}

def _vless_api(server_id: int) -> AsyncApi:
    return AsyncApi(
        f"http://{vless_server_ip[server_id]}:{VLESS_PORT}{VLESS_URI}",
        VLESS_USERNAME, VLESS_PASSWORD, proxy=VLESS_PROXY,
    )

vless_client = {
    11: _vless_api(11),
    31: _vless_api(31),
    70: _vless_api(70),
    81: _vless_api(81),
    91: _vless_api(91),
    110: _vless_api(110),
    50: _vless_api(50),
    60: _vless_api(60),
    40: _vless_api(40),
    120: _vless_api(120),
    130: _vless_api(130),
}

servers_countries = {
    11: "Россия",
    31: "Германия",
    70: "Латвия",
    81: "Нидерланды",
    91: "Финляндия",
    110: "Австрия",
    50: "Великобритания",
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
    50: "Great-Britain",
    60: "USA",
    40: "France",
    120: "Turkey",
    130: "Hong-Kong",
}

parameters = {
    11: {
        "type": "tcp",
        "security": "reality",
        "pbk": "lAScRU8jMDzUw5Ye4U7sPKCNW1m7Yfkow9Cr9HjFYDM",
        "fp": "random",
        "sni": "duma.gov.ru",
        "sid": "bc50e9ab90b2114c",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    110: {
        "type": "tcp",
        "security": "reality",
        "pbk": "wBcFJbtbh6eaEDZiGq581AeTlu03PGS5BUIaQvgiQiw",
        "fp": "random",
        "sni": "www.apple.com",
        "sid": "adde4c1289db8d57",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    50: {
        "type": "tcp",
        "security": "reality",
        "pbk": "C8J4nK_U-MPhlHXieNjgi07SE3sro_Np5fT0tAignUI",
        "fp": "random",
        "sni": "www.apple.com",
        "sid": "25ce",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
   91: {
        "type": "tcp",
        "security": "reality",
        "pbk": "cvMJWqzKGfZKX4gZErncuBXOqjONYB1Vto3t_SHZwlY",
        "fp": "random",
        "sni": "www.amazon.com",
        "sid": "3b3bb98d4590da",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    81: {
        "type": "tcp",
        "security": "reality",
        "pbk": "zDiuJ9Vx7ggfU2BS3D6HkrzOfK_iWopKAPLETWGdo00",
        "fp": "random",
        "sni": "www.apple.com",
        "sid": "c0",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    70: {
        "type": "tcp",
        "security": "reality",
        "pbk": "emcMwsdB_016scSUXhauN6VzlAegwebNL4MnC1mja1Q",
        "fp": "random",
        "sni": "www.apple.com",
        "sid": "db7b45464fc4f9b3",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    31: {
        "type": "tcp",
        "security": "reality",
        "pbk": "6oVLpEgrYEAeCYekJD3Cgt3BWqcmvuQzMLxPSy4xTiE",
        "fp": "random",
        "sni": "www.icloud.com",
        "sid": "dd1a0469ba41",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
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
        "sni": "aws.amazon.com",
        "sid": "e3b346af",
        "spx": "%2F",
        "flow": "xtls-rprx-vision"
    },
    120: {
        "type": "tcp",
        "security": "reality",
        "pbk": "6knpCNBHicI-jW-0PXAy18RVkFJv3Ies3OEhMYikFDU",
        "fp": "random",
        "sni": "aws.amazon.com",
        "sid": "a7d8216819",
        "spx": "%2F",
        "pqv": "HhRDZY4N2keGPWVTtIVAE-0mxT8BON4ZWvERC1h1kxAH3fSK0B2oNY2dIjl8rZ5PDxiXGl2V6WRsWHJKosvCA35DG291lapcpXwGr3Koour2HtoV2tCBYuI1CfUadooN5Gfz8yDKwVZPSX1BjHqjKDRf_tyqunP_wsluIiZS6QdY9iow9BaxAdfRjdV-8OcxSfrYcDtB7zeEA3mdEQAPTmRIDaeBMmW1eA-2AmvCManA4mLO2wPp8oI3WIF2qYVitn08gcGbpZp2ipTYNO8aq-LaaSczpD1avDXzKwKT21BhZ39p7trdWA5cfYLFCTb3XQQi6B9Pi7WbyO2CPianQ-q-Va5QNqJPuUr60fwGfac0LCNeTjNi_4cP9Q0leKBu1gqOzr-FOkFBt0Q3feJczRm5AiI37FHKhTTt5KBKoI3kvCP3cC-tngSVdfcMmb0fC7vY6Fl3oLJ2O6Rip6sBrfVCRQCb5Mja3B6I7QN_FzBS2lFMqmjr-8j8wS5dHTjCXOgPbOMGcJSsciMf2zerWBOF0XryFxYmXD7hpG08MqbMyYLlUbHmHdjHFp5T6kkLwtRVALx9lWw29r1gi-ij0bBxkM6qXwIJay1PaghO_4bWaLKrjSlksfbdLCKkM13rnjDN8Ed81KG4MskKLfx9KbhF9ely5MJOmHbwbOMU5Rj3KpODn7bMFPFD8EvigphHy_zrTOs-Iv-JAdhhRrszSsG3dPT1dU5Z_UVXv9sKl-canzmNcMxPqcnkEMkGVc_9WB6bXuMVCC_Rp4KraHl8C6DLopPIQPGD87mevib2VLU4_UxX3XPuinis7T5GgtQhqxHY1yzdRhXYAquuKu2lCjFNZQhg6gHm6gV-3KYNpcbjm_c5Gka2C0osLqHbGIGhfBbrOEg-Vs3HQTwGeRPrbdGGG4iNzFf6G4-8y8QZd2JbifRIWnbsv_ILWw6laMLNHBYDJURR7caNVZCbmHQyduGDFQG_NkPANzTeW6Rf8ngyywUQQafA-dp8_ShGyTU8cSEZe6kT3dmkx_m07UWOyCKNITw4EgAFCfzE2GFvvcHozFtaMHsyZH-ZVIGRobs5SwKZF0BypLzV1jOZ6H_d8VDVRyycz3GvdIUcVmcCtf7GE6iSvPAttBLsrOF8iAeOiGcA73y-JI3rB-ZQDDSCTZIsLg6BD3rID_yKdWRuq9ciRODt7GMoUv8C2jQKF37xChh8d0ck7ZX4-vRS3BbxDFfXx2ls9YTK6Elo1C0DkXKZeo9OtawA5RUj-M0Qy9sziHb18qbhSsRNtb2xQDNzzNUY2UYRACxSowalY-0edFpkW7fFLEACIpJuhwPmZFQiuUCkL7vtNCasB3ogz0yAks4E5E1o2-XFeBT5feqBY5h1sq8RibZOIuYz123YDIySww0ebIhDFKQY6DXxzMRr4sQlCzS1d5FhxjIsORJSjR7VvhqD2-Muiv9_Ata5Xw7gjgLM8kcM-exmVlZ4D1UsViLZNbh1SOXrVS9opKkJCfqRuRggiuWBgCJTPXafO-GV3vJqnHXZxxWMGUWnReyrFPocdPspOVyvnHOZzUU5QS13MPUvbPow5-S_c6zvNgNOOsZ1PTrPQXymTl62RazizJ0pbByR1Jq7EWv54aEUwxRdhziQGQx9aWI75kz2yl490HHXY5ct6cYwQ2jzqf9NWTzgv2dLhUL0yqMH_to8HsU-qicZHgLjBlvDAd0CUF5pKTQqYabla07ilXuDmEMTkPMItYz2ZeZkLaI_bUlsS0LuqYLGM48ynS2QdzG4-0JSk9s8OyVy2ycDYBOKjOae_jdLMl4Vv0NMzYmv_G6JdpEK60C7xPe-xJxUSgCa1YUVqAAdB2MTKjuyCdVTIsQ49NuJ1JqoKZjrS9IOoyAUFC9mN9B9g2rbqAuQqvS0kszAZo_k-0p8iaahz_SBk1RUWkWCeKo4yyha6PIPmk-HtP4jLDC5hCHzMRLYKjUr8OZgj4qPwaAiFayr1MZPg6ld0zhAWXB6bJRuY66BkXuj__P8wpaZiVXesnEi_QGEI15RrmtS4iTRn3OlTdBPMopx5XszHIHBZ6Mh_B3dV_pubexnWrerBWBv0jARKDH6KvQGkY5UqDdbj4Hdp39cgQR-_vybQnTznvQ3a7367wjZvqGVTaXhHI__FRSpow4hjMlT3-jbspHJaE5DON3dyE9UkCPksx-k8g-NKhNABG3SSVTIaXItPpUwUetzXYR9wQo2A3Z_rQJbwI18flBLdj00HsHfg3FKXbkeuGBjNnLHObwCNURtcEeqJoVfkvnvyuh7JxmgPdY9k5VMHIDhuSP5Xw-iFMxPSufqhGPKRyLZ91gaH3Ho_wCYX3Q28drk4tfuaOHjPqzfhYUL0EkC7VKEpZ0i_q_dC1jt1IcerlpC-pMfm6YB8jLPv0ci7VXVq9Z4rVA6rpgnZG4Pt0oZAZkCo8FcYyQG-0hYDE6Iw-k93e7KxBbiPHVVXlBQP_zT-QRX9UD3nZKsO1BQrrdjguVh6xw2e-_Md_nFpWZkzbXsCQ9XWhEuvOoifa6xEP5E5RaLErSthb8HlLpbz-Nwf22cCHWXv68-9M-2JAQqJr-vLfA",
        "flow": "xtls-rprx-vision"
    },
    130: {
        "type": "tcp",
        "security": "reality",
        "pbk": "E1AAVc6eZDpW69olGjPxK89-NB2enVox5w5oA8YHLCM",
        "fp": "random",
        "sni": "www.nvidia.com",
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
    50: 1,
    60: 1,
    40: 1,
    120: 1,
    130: 1,
}


SSCONF = "ssconf"
KEYS_URL = SSCONF + "://" + DOMEN + "/keys" + "/"
VLESS_URL = "https://" + DOMEN + "/vless/"
