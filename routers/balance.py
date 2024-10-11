from aiogram import filters, types, Router

from database.models import User, Transaction
from database.engine import SessionLocal

from sqlalchemy import select

router = Router(name=__name__)


@router.message(filters.Command("profile"))
async def on_profile_command(message: types.Message) -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=str(message.from_user.id)))

        user = result.scalar()

        if not user:
            session.add(User(telegram_id=str(message.from_user.id), balance=0))
            await session.commit()

            result = await session.execute(select(User).filter_by(telegram_id=str(message.from_user.id)))

            user = result.scalar()
        
        await message.answer(
            text=f"🎂 <b>Профиль {message.from_user.first_name} [{user.id}]</b>"
                f"\n🪙 <b>Баланс:</b> {user.balance}"
        )
