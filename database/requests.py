from database.models import async_session
from database.models import Arendator, House
from sqlalchemy import select, delete


async def get_user_by_name(name):
    async with async_session() as session:
        return await session.scalar(select(Arendator).where(Arendator.name == name))


async def get_user_by_tg_id(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Arendator).where(Arendator.tg_id == tg_id))


async def add_user(tg_id, name, phone, username):
    async with async_session() as session:
        user = await session.scalar(select(Arendator.tg_id == tg_id))

        if not user:
            session.add(Arendator(tg_id=tg_id, name=name, phone=phone, username=username))
            await session.commit()


async def add_object(tg_id, city, area, adress):
    async with async_session() as session:
        user = await session.scalar(select(House.adress == adress))

        if not user:
            session.add(House(arendator=tg_id, city=city, area=area, adress=adress))
            await session.commit()


async def get_houses(tg_id):
    async with async_session() as session:
        return await session.scalars(select(House).where(House.arendator == tg_id))


async def all_houses():
    async with async_session() as session:
        return await session.scalars(select(House))


async def all_houses_by_city(city):
    async with async_session() as session:
        return await session.scalars(select(House).where(House.city == city))


async def all_houses_by_areas(area):
    async with async_session() as session:
        return await session.scalars(select(House).where(House.area == area))


async def get_house_info(house_id):
    async with async_session() as session:
        return await session.scalar(select(House).where(int(house_id) == House.id))


async def delete_my_account(tg_id):
    async with async_session() as session:
        result = await session.execute(delete(Arendator).where(Arendator.tg_id == tg_id))
        if result.rowcount > 0:
            await session.commit()
            print(f"Аккаунт пользователя с tg_id={tg_id} успешно удален.")
        else:
            print(f"Пользователь с tg_id={tg_id} не найден.")
