import asyncio

from yookassa import Configuration

from config import SECRET_KEY, SHOP_ID, bot, dp
from handlers import buy_router, info_router, main_router, profile_router
from handlers.admin import admin_router

dp.include_router(admin_router)
dp.include_router(buy_router)
dp.include_router(profile_router)
dp.include_router(info_router)
dp.include_router(main_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    Configuration.account_id = SHOP_ID
    Configuration.secret_key = SECRET_KEY

    asyncio.run(main())
