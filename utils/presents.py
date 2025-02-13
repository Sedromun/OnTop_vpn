from database.controllers.present import create_present_db
from aiogram.utils.deep_linking import create_start_link
from config import bot


async def create_present(user_id, duration, country, price):
    present = create_present_db(
            {
                "user_id": user_id,
                "country": country,
                "price": price,
                "duration": duration
            }
        )

    link = await create_start_link(bot, present.id, encode=True)
    

