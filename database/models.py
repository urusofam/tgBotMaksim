from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv('SQL_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Arendator(Base):
    __tablename__ = 'arendators'
    tg_id = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[str] = mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))


class House(Base):
    __tablename__ = 'houses'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100))
    adress: Mapped[str] = mapped_column(String(100))
    reports: Mapped[str] = mapped_column(String(100))
    guests: Mapped[str] = mapped_column(String(100))
    book: Mapped[str] = mapped_column(String(100))
    reviews: Mapped[str] = mapped_column(String(100))
    agreement: Mapped[str] = mapped_column(String(100))
    arendator = mapped_column(ForeignKey('arendators.tg_id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
