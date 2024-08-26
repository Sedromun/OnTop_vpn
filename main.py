import asyncio

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from config import bot, dp, FERNET
from database.controllers.order import get_order
from handlers import buy_router, info_router, main_router, profile_router
from handlers.admin import admin_router
from servers.outline_keys import get_key

dp.include_router(admin_router)
dp.include_router(buy_router)
dp.include_router(profile_router)
dp.include_router(info_router)
dp.include_router(main_router)

app = FastAPI()


@app.get("/keys/{order_id_enc}")
async def get_key_id(order_id_enc: str):
    order_id = FERNET.decrypt(order_id_enc.encode()).decode()
    order = get_order(int(order_id))
    key = get_key(order.country, order_id)
    return HTMLResponse(key)


@app.get("/")
async def root():
    return "Hello!"


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
