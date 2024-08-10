from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Arendator(Base):
    __tablename__ = 'arendators'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(50))
    tg_id = mapped_column(BigInteger)

class Houses(Base):
    __tablename__ = 'houses'

    id: Mapped[int] = mapped_column(primary_key=True)
    adress: Mapped[str] = mapped_column(String(100))
    reports: Mapped[str] = mapped_column(String(100))
    quests: Mapped[str] = mapped_column(String(100))
    book: Mapped[str] = mapped_column(String(100))
    reviews: Mapped[str] = mapped_column(String(100))
    arendator: Mapped[int] = mapped_column(ForeignKey('arendators.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)