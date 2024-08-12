import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from config import bot, dp, HOST, PORT
from database.controllers.order import get_order

from handlers import main_router, buy_router, profile_router, info_router
from servers.outline_keys import get_key

dp.include_router(buy_router)
dp.include_router(main_router)
dp.include_router(profile_router)
dp.include_router(info_router)

app = FastAPI()

@app.get("/keys/{order_id}")
async def get_key_id(
        order_id: int
):
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
