import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

BOT_TOKEN: SecretStr = SecretStr(os.getenv("BOT_TOKEN"))
DB_USER = str(os.getenv("DB_USER"))
DB_URL = str(os.getenv("DB_URL"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))
PAYMENTS_PROVIDER_TOKEN = str(os.getenv("PAYMENTS_PROVIDER_TOKEN"))
MIN_ADD_AMOUNT = 90
SUPPORT_TAG = str(os.getenv("SUPPORT_TAG"))
RECALLS_TGC_TAG = str(os.getenv("RECALLS_TGC_TAG"))
RECALLS_TGC_LINK = "https://t.me/" + RECALLS_TGC_TAG
CONNECT_INSTR_URL = str(os.getenv("CONNECT_INSTR_URL"))
bot = Bot(BOT_TOKEN.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()

