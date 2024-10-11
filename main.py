from aiogram import Bot, Dispatcher, Router, types, enums, filters, methods
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import logging
import sys

from routers.balance import router as balance_router

from config import TOKEN

from database.models import User
from database.engine import SessionLocal

from sqlalchemy import select


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

dp = Dispatcher(storage=MemoryStorage())


@dp.message(filters.CommandStart())
async def on_command_start(message: types.Message) -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=str(message.from_user.id)))

        user = result.scalar()

        if not user:
            print('Пользователя нет добавляем')
            session.add(User(telegram_id=str(message.from_user.id), balance=0))
            await session.commit()

            result = await session.execute(select(User).filter_by(telegram_id=str(message.from_user.id)))

            user = result.scalar()
        else:
            print('Пользователь есть')
        
    await message.answer(
        text=f"<b>Здравствуй, {message.from_user.first_name}</b>\n"
            "Добро пожаловать в игру!"
    )

async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=enums.ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp.include_routers(balance_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
