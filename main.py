from aiogram import Bot, Dispatcher, Router, types, enums, filters, methods
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import logging
import sys

from config import TOKEN


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

dp = Dispatcher(storage=MemoryStorage())


@dp.message(filters.CommandStart())
async def on_command_start(message: types.Message) -> None:
    await message.answer(
        text=f"<b>Здравствуй, {message.from_user.first_name}</b>\n"
            "Добро пожаловать в игру!"
    )

@dp.message()
async def on_message(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Тише дочка")


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=enums.ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
