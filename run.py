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
    house_info = await rq.get_house_info(callback.data.split('_')[2])
    choice = callback.data.split('_')[1]
    if choice == 'obj':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'Вам добавлен объект: {house_info.adress}. Можете ознакомиться с актуальной ' +
                                    f'информацией по нему в разделе "Мои объекты"')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'guests':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена ' +
                                    f'новая информация в разделе гостей')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'bron':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе ' +
                                    f'бронирования')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'reports':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена ' +
                                    f'новая информация в разделе отчётов')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'reviews':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая ' +
                                    f'информация в разделе отзывов')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'agreement':
        await bot.send_message(chat_id=house_info.arendator,
                               text=f'По вашему объекту {house_info.adress} добавлена новая информация в разделе ' +
                                    f'договора')
        await callback.message.delete()
        await callback.message.answer('Вы отправили оповещение')
    elif choice == 'other':
        await callback.message.edit_text('Напишите ваше сообщение')
        await state.set_state(Report.text)
        await state.update_data(adress=house_info.adress, tg_id=house_info.arendator)


@dp.message(Report.text)
async def report_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=data['tg_id'], text=f'Объект: {data['adress']}\nСообщение: {data['text']}')
    await message.answer('Вы отправили оповещение')
    await state.clear()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
