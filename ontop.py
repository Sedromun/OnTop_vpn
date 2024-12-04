import asyncio

from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile

from config import ontop_dp, ontop_bot


@ontop_dp.message(StateFilter(None))
async def incorrect_command_handler(message: Message):
    logo = FSInputFile("photos/logo.jpg")
    await message.answer_document(
        logo,
        caption="Мы провели ребрендинг и переехали в нового бота⚡️\n\n"
        "<b>Этот бот больше не работает!</b>\n\n"
        "Ждём вас в @cliquevpnbot\n\n"
        "<i>P.S. Если у вас была оформлена подписка, но вы еще не пользовались новым ботом, напишите нам в поддержку "
        "@cliquevpn_support</i>"
    )


async def main():
    await ontop_bot.delete_webhook(drop_pending_updates=True)
    await ontop_dp.start_polling(ontop_bot)


if __name__ == "__main__":
    asyncio.run(main())
