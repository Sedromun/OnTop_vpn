import asyncio

from fastapi import FastAPI
from yookassa import Configuration

from config import SECRET_KEY, SHOP_ID, bot, dp, vless_client
from handlers import buy_router, info_router, main_router, profile_router
from handlers.admin import admin_router

dp.include_router(admin_router)
dp.include_router(buy_router)
dp.include_router(profile_router)
dp.include_router(info_router)
dp.include_router(main_router)

app = FastAPI()


async def main():
    for api in vless_client.values():
        await api.login()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = SECRET_KEY

    asyncio.run(main())
