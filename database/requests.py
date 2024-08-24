from database.models import async_session, Arendator, House
from sqlalchemy import select, update, delete


async def get_user_by_name(name):
    async with async_session() as session:
        return await session.scalar(select(Arendator).where(Arendator.name == name))


async def get_user_by_tg_id(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Arendator).where(Arendator.tg_id == tg_id))


async def add_user(tg_id, name, phone, username='NULL'):
    async with async_session() as session:
        user = await session.scalar(select(Arendator.tg_id == tg_id))

        if not user:
            session.add(Arendator(tg_id=tg_id, name=name, phone=phone, username=username))
            await session.commit()


async def update_object(choice, url, house_id):
    async with async_session() as session:
        if choice == 0:
            await session.execute(update(House).where(int(house_id) == House.id).values(book=url))
        elif choice == 1:
            await session.execute(update(House).where(int(house_id) == House.id).values(guests=url))
        elif choice == 2:
            await session.execute(update(House).where(int(house_id) == House.id).values(reports=url))
        elif choice == 3:
            await session.execute(update(House).where(int(house_id) == House.id).values(agreement=url))
        elif choice == 4:
            await session.execute(update(House).where(int(house_id) == House.id).values(reviews=url))
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
        await session.execute(delete(House).where(House.arendator == tg_id))
        await session.execute(delete(Arendator).where(Arendator.tg_id == tg_id))
        await session.commit()

async def delete_object(house_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(delete(House).where(House.id == house_id))
            await session.commit()
            if result.rowcount > 0:
                return True
            else:
                return False
