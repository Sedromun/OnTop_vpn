import os

from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from pydantic import SecretStr
from cryptography.fernet import Fernet
from yookassa import Configuration

from outline.outline_vpn.outline_vpn import OutlineVPN

load_dotenv()

BOT_TOKEN: SecretStr = SecretStr(os.getenv("BOT_TOKEN"))

DB_USER = str(os.getenv("DB_USER"))
DB_URL = str(os.getenv("DB_URL"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))

HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))

DOMEN = str(os.getenv("DOMEN"))

SWEDEN_API_URL = str(os.getenv("SWEDEN_API_URL"))
SWEDEN_CERT_SHA256 = str(os.getenv("SWEDEN_CERT_SHA256"))

RUSSIAN_API_URL = str(os.getenv("RUSSIAN_API_URL"))
RUSSIAN_CERT_SHA256 = str(os.getenv("RUSSIAN_CERT_SHA256"))

GERMAN_API_URL = str(os.getenv("GERMAN_API_URL"))
GERMAN_CERT_SHA256 = str(os.getenv("GERMAN_CERT_SHA256"))

FRANCE_API_URL = str(os.getenv("FRANCE_API_URL"))
FRANCE_CERT_SHA256 = str(os.getenv("FRANCE_CERT_SHA256"))

GB_API_URL = str(os.getenv("GB_API_URL"))
GB_CERT_SHA256 = str(os.getenv("GB_CERT_SHA256"))

USA_API_URL = str(os.getenv("USA_API_URL"))
USA_CERT_SHA256 = str(os.getenv("USA_CERT_SHA256"))

LATVIA_API_URL = str(os.getenv("LATVIA_API_URL"))
LATVIA_CERT_SHA256 = str(os.getenv("LATVIA_CERT_SHA256"))

ESTONIA_API_URL = str(os.getenv("ESTONIA_API_URL"))
ESTONIA_CERT_SHA256 = str(os.getenv("ESTONIA_CERT_SHA256"))

NETHERLAND_API_URL = str(os.getenv("NETHERLAND_API_URL"))
NETHERLAND_CERT_SHA256 = str(os.getenv("NETHERLAND_CERT_SHA256"))

FINLAND_API_URL = str(os.getenv("FINLAND_API_URL"))
FINLAND_CERT_SHA256 = str(os.getenv("FINLAND_CERT_SHA256"))

AUSTRIA_API_URL = str(os.getenv("AUSTRIA_API_URL"))
AUSTRIA_CERT_SHA256 = str(os.getenv("AUSTRIA_CERT_SHA256"))

HTTPS = "https"
SSCONF = "ssconf"
KEYS_URL = SSCONF + "://" + DOMEN + "/keys" + "/"

outline_client = {
    "Россия": OutlineVPN(api_url=RUSSIAN_API_URL, cert_sha256=RUSSIAN_CERT_SHA256),
    "Швеция": OutlineVPN(api_url=SWEDEN_API_URL, cert_sha256=SWEDEN_CERT_SHA256),
    "Германия": OutlineVPN(api_url=GERMAN_API_URL, cert_sha256=GERMAN_CERT_SHA256),
    "Франция": OutlineVPN(api_url=FRANCE_API_URL, cert_sha256=FRANCE_CERT_SHA256),
    "Великобритания": OutlineVPN(api_url=GB_API_URL, cert_sha256=GB_CERT_SHA256),
    "США": OutlineVPN(api_url=USA_API_URL, cert_sha256=USA_CERT_SHA256),
    "Латвия": OutlineVPN(api_url=LATVIA_API_URL, cert_sha256=LATVIA_CERT_SHA256),
    "Нидерланды": OutlineVPN(api_url=NETHERLAND_API_URL, cert_sha256=NETHERLAND_CERT_SHA256),
    "Финляндия": OutlineVPN(api_url=FINLAND_API_URL, cert_sha256=FINLAND_CERT_SHA256),
    "Эстония": OutlineVPN(api_url=ESTONIA_API_URL, cert_sha256=ESTONIA_CERT_SHA256),
    "Австрия": OutlineVPN(api_url=AUSTRIA_API_URL, cert_sha256=AUSTRIA_CERT_SHA256),
}

PAYMENTS_PROVIDER_TOKEN = str(os.getenv("PAYMENTS_PROVIDER_TOKEN"))
MIN_ADD_AMOUNT = 90
TECH_SUPPORT_TAG = str(os.getenv("TECH_SUPPORT_TAG"))
TECH_SUPPORT_LINK = "https://t.me/" + TECH_SUPPORT_TAG
RECALLS_TGC_TAG = str(os.getenv("RECALLS_TGC_TAG"))
RECALLS_TGC_LINK = "https://t.me/" + RECALLS_TGC_TAG
INSTR_URL = str(os.getenv("INSTR_URL"))

CRYPTO_KEY = str(os.getenv("CRYPTO_KEY"))

FERNET = Fernet(CRYPTO_KEY)

bot = Bot(BOT_TOKEN.get_secret_value(), parse_mode="HTML", disable_web_page_preview=True)

dp = Dispatcher()

WELCOME_PHOTO = FSInputFile("photos/welcome.jpg")
BUY_PHOTO = FSInputFile("photos/buy.jpg")
INFO_PHOTO = FSInputFile("photos/info.jpg")
PROFILE_PHOTO = FSInputFile("photos/profile.jpg")

PERCENT_REFERRAL = 10
WELCOME_PRESENT = 50
BOT_LINK = "https://t.me/OnTop_vpn_bot"
REFS_PARAM = "?start="

INTERVAL = 5  # mins

SAVVA_ADMIN = str(os.getenv("SAVVA_ADMIN"))
EVGENIY_ADMIN = str(os.getenv("EVGENIY_ADMIN"))
TECH_SUPPORT_ADMIN = str(os.getenv("TECH_SUPPORT_ADMIN"))

ADMINS = [SAVVA_ADMIN, EVGENIY_ADMIN, TECH_SUPPORT_ADMIN]

ONE_DAY_SALE = 30


SHOP_ID = str(os.getenv("SHOP_ID"))
SECRET_KEY = str(os.getenv("SECRET_KEY"))



BOT_URL = str(os.getenv("BOT_URL"))
