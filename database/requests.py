from database.models import async_session
from database.models import Arendator
from sqlalchemy import select, update, delete

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Arendator).where(Arendator.tg_id == tg_id))

        if not user:
         session.add(Arendator(tg_id=tg_id))
         await session.commit()

async def add_user(tg_id, name, phone):
    async with async_session() as session:
        user = await session.scalar(select(Arendator.tg_id == tg_id))

        if not user:
            session.add(Arendator(tg_id=tg_id, name=name, phone=phone))
            await session.commit()