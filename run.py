import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

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


@dp.callback_query(F.data.startswith('report_'))
async def report_arendator(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы отправили оповещение')
    house_info = await rq.get_house_info(callback.data.split('_')[2])
    if callback.data.split('_')[1] == 'guests':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе гостей')
    elif callback.data.split('_')[1] == 'bron':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе бронирования')
    elif callback.data.split('_')[1] == 'reports':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе отчётов')
    elif callback.data.split('_')[1] == 'reviews':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе отзывов')
    elif callback.data.split('_')[1] == 'agreement':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе договора')
    elif callback.data.split('_')[1] == 'other':
        await callback.message.edit_text('Напишите ваше сообщение')
        await state.set_state(Report.text)
        await state.update_data(adress=house_info.adress, tg_id=house_info.arendator)
    await callback.message.delete()


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
