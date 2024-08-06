import asyncio

from config import bot, dp

from handlers import main_router, buy_router, profile_router, info_router

dp.include_router(buy_router)
dp.include_router(main_router)
dp.include_router(profile_router)
dp.include_router(info_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
