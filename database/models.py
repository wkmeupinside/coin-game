from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy import String, BigInteger, ForeignKey, TIMESTAMP, func

from typing import List


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str] = mapped_column(String(255), unique=True)
    balance: Mapped[int] = mapped_column(BigInteger())

    transactions_sent: Mapped[List["Transaction"]] = relationship(back_populates="sender")
    transactions_recieved: Mapped[List["Transaction"]] = relationship(back_populates="reciever")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reciever_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(BigInteger())
    timestamp: Mapped[str] = mapped_column(TIMESTAMP(), server_default=func.now())

    sender: Mapped["User"] = relationship(back_populates="transactions_sent")
    reciever: Mapped["User"] = relationship(back_populates="transactions_recieved")
