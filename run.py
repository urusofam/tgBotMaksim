import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from admin.handlers import router_admin
from database.models import async_main
from handlers.handlers import router
import database.requests as rq


class Report(StatesGroup):
    text = State()
    adress = State()
    tg_id = State()


load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(router)
dp.include_router(router_admin)


async def main():
    await async_main()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.callback_query(F.data.startswith('guests_'))
async def report_guests(callback: CallbackQuery):
    await callback.message.answer('Вы отправили оповещение.')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await bot.send_message(chat_id=house_info.arendator,
                           text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе гостей')
    await callback.message.delete()


@dp.callback_query(F.data.startswith('bron_'))
async def report_bron(callback: CallbackQuery):
    await callback.message.answer('Вы отправили оповещение.')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await bot.send_message(chat_id=house_info.arendator,
                           text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе бронирования')
    await callback.message.delete()


@dp.callback_query(F.data.startswith('reports_'))
async def report_reports(callback: CallbackQuery):
    await callback.message.answer('Вы отправили оповещение.')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await bot.send_message(chat_id=house_info.arendator,
                           text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе отчётов')
    await callback.message.delete()


@dp.callback_query(F.data.startswith('reviews_'))
async def report_reviews(callback: CallbackQuery):
    await callback.message.answer('Вы отправили оповещение.')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await bot.send_message(chat_id=house_info.arendator,
                           text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе отзывов')
    await callback.message.delete()


@dp.callback_query(F.data.startswith('agreement_'))
async def report_agreement(callback: CallbackQuery):
    await callback.message.answer('Вы отправили оповещение.')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await bot.send_message(chat_id=house_info.arendator,
                           text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе договора')
    await callback.message.delete()


@dp.callback_query(F.data.startswith('other_'))
async def report_other(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Напишите ваше сообщение')
    house_info = await rq.get_house_info(callback.data.split('_')[1])
    await state.set_state(Report.text)
    await state.update_data(adress=house_info.adress, tg_id=house_info.arendator)


@dp.message(Report.text)
async def report_text(message: Message, state):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=data['tg_id'], text=f'Объект: {data['adress']}\nСообщение: {data['text']}')
    await state.clear()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
