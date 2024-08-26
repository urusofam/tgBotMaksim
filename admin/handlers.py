import aiogram.exceptions
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import os
from dotenv import load_dotenv
import admin.keyboards as kb
import database.requests as rq

router_admin = Router()
load_dotenv()


class Find(StatesGroup):
    name = State()
    choice = State()
    last_msg = State()


class Reviews(StatesGroup):
    url = State()
    house_id = State()


class Guests(StatesGroup):
    url = State()
    house_id = State()


class Book(StatesGroup):
    url = State()
    house_id = State()


class Reports(StatesGroup):
    url = State()
    house_id = State()


class Agreement(StatesGroup):
    url = State()
    house_id = State()


class Add(StatesGroup):
    name = State()
    city = State()
    area = State()
    adress = State()


class House(StatesGroup):
    city = State()
    area = State()
    adress = State()


@router_admin.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Добро пожаловать в админ панель', reply_markup=kb.admin_menu)


@router_admin.message(F.text == 'Связаться с собственником')
async def ask_method(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=await kb.find_menu(0))
        await state.update_data(last_msg=message.message_id)


@router_admin.message(F.text == 'Редактировать объект')
async def redact_object(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=await kb.find_menu(3))
        await state.update_data(last_msg=message.message_id)


@router_admin.message(F.text == 'Добавить объект')
async def add_object_arendator(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.set_state(Add.name)
        msg = await message.answer('Введите ФИО собственника')
        await state.update_data(msg_id=msg.message_id)


@router_admin.callback_query(F.data.startswith('find_fio_'))
async def ask_fio(callback: CallbackQuery, state: FSMContext):
    choice = callback.data.split('_')[2]
    if choice == '0': await state.update_data(choice=0)
    elif choice == '1': await state.update_data(choice=1)
    elif choice == '3': await state.update_data(choice=3)
    await callback.message.delete()
    msg = await callback.message.answer('Введите ФИО')
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Find.name)


@router_admin.message(Find.name)
async def find_user(message: Message, state: FSMContext):
    person = await rq.get_user_by_name(message.text)
    data = await state.get_data()
    await message.delete()
    await message.chat.delete_message(data['msg_id'])
    if data['choice'] == 0:
        if person:
            await message.answer('@' + person.username + '\n' + person.phone, reply_markup=kb.admin_menu)
        else:
            await message.answer('Собственник не найден', reply_markup=kb.admin_menu)
        await state.clear()
    elif data['choice'] == 1:
        if person:
            await message.answer('Выберите его объект', reply_markup=await kb.houses_arendator(2, person.tg_id))
        else:
            await message.answer('Собственник не найден', reply_markup=kb.admin_menu)
            await state.clear()
    elif data['choice'] == 3:
        if person:
            await message.answer('Выберите его объект', reply_markup=await kb.houses_arendator(3, person.tg_id))
        else:
            await message.answer('Собственник не найден', reply_markup=kb.admin_menu)
            await state.clear()


@router_admin.message(Add.name)
async def ask_add_name(message: Message, state: FSMContext):
    arendator = await rq.get_user_by_name(message.text)
    if arendator:
        data = await state.get_data()
        await message.chat.delete_message(data['msg_id'])
        await message.delete()
        await state.update_data(name=arendator.tg_id)
        msg = await message.answer('Выберите город', reply_markup=kb.cities_menu)
        await state.update_data(msg_id=msg.message_id)
    else:
        data = await state.get_data()
        await message.chat.delete_message(data['msg_id'])
        await message.delete()
        await state.clear()
        await message.answer('Собственник не найден')


@router_admin.callback_query(F.data == 'spb')
async def ask_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(city='Санкт-Петербург')
    await callback.message.edit_text('Введите район', reply_markup=kb.back_out)
    await state.set_state(Add.area)


@router_admin.callback_query(F.data == 'another')
async def ask_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите город', reply_markup=kb.back_out)
    await state.set_state(Add.city)


@router_admin.message(Add.city)
async def ask_add_city(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.chat.delete_message(data['msg_id'])
    await message.delete()
    await state.update_data(city=message.text)
    msg = await message.answer('Введите район', reply_markup=kb.back_out)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Add.area)


@router_admin.message(Add.area)
async def ask_add_area(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.chat.delete_message(data['msg_id'])
    await message.delete()
    await state.update_data(area=message.text)
    msg = await message.answer('Введите адрес', reply_markup=kb.back_out)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Add.adress)


@router_admin.message(Add.adress)
async def write_object(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    data = await state.get_data()
    await message.chat.delete_message(data['msg_id'])
    await message.delete()
    result = await rq.add_object(data['name'], data['city'], data['area'], data['adress'])
    arendator = await rq.get_user_by_tg_id(data['name'])
    if result:
        await message.answer(f"Вы добавили объект:\nСобственник: {arendator.name}\nГород: {data['city']}\n" +
                             f"Район: {data['area']}\nАдрес: {data['adress']}",
                             reply_markup=kb.admin_menu)
    else:
        await message.answer('Этот объект уже существует', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(F.text == 'Оповещения собственников')
async def alerts(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=await kb.find_menu(1))
        await state.update_data(msg_id=message.message_id)


@router_admin.callback_query(F.data.startswith('arendator_house'))
async def house_arendator(callback: CallbackQuery):
    if callback.data.split('_')[2] == '1' or callback.data.split('_')[2] == '2':
        await callback.message.edit_text('Выберите что вам нужно',
                                         reply_markup=await kb.reports(callback.data.split('_')[3]))
    elif callback.data.split('_')[2] == '0':
        house = await rq.get_house_info(callback.data.split('_')[3])
        arendator = await rq.get_user_by_tg_id(house.arendator)
        if arendator:
            await callback.message.edit_text('@' + arendator.username + '\n' + arendator.phone)
        else:
            await callback.message.edit_text('Собственник не найден')
    elif callback.data.split('_')[2] == '3':
        await callback.message.edit_text('Выберите что вы хотите отредактировать',
                                         reply_markup=await kb.houses_info_menu_admin(callback.data.split('_')[3]))


@router_admin.callback_query(F.data.startswith('redact_'))
async def redact_house(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    house_id = callback.data.split('_')[2]
    if action == 'reviews':
        await callback.message.edit_text('Напишите ссылку на отзывы', reply_markup=kb.back_out)
        await state.set_state(Reviews.url)
    elif action == 'guests':
        await callback.message.edit_text('Напишите ссылку на сканы договоров с гостями', reply_markup=kb.back_out)
        await state.set_state(Guests.url)
    elif action == 'book':
        await callback.message.edit_text('Напишите ссылку на таблицу с бронированиями', reply_markup=kb.back_out)
        await state.set_state(Book.url)
    elif action == 'reports':
        await callback.message.edit_text('Напишите ссылку на отчёты', reply_markup=kb.back_out)
        await state.set_state(Reports.url)
    elif action == 'agreement':
        await callback.message.edit_text('Напишите ссылку на текущий договор с собственником', reply_markup=kb.back_out)
        await state.set_state(Agreement.url)
    elif action == 'delete':
        await callback.message.edit_text('Подтвердите удаление', reply_markup=await kb.confirm_menu(house_id))
    await state.update_data(house_id=house_id)


@router_admin.callback_query(F.data.startswith('confirm_delete_'))
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    house_id = callback.data.split('_')[2]
    await rq.delete_object(house_id)
    await callback.message.edit_text('Объект успешно удалён')
    await state.clear()


@router_admin.callback_query(F.data == 'cancel_delete')
async def cancel_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Удаление отменено.', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Reviews.url)
async def redact_reviews(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    await rq.update_object(0, data['url'], data['house_id'])
    await message.answer('Объект успешно отредактирован', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Guests.url)
async def redact_guests(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    await rq.update_object(1, data['url'], data['house_id'])
    await message.answer('Объект успешно отредактирован', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Book.url)
async def redact_book(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    await rq.update_object(2, data['url'], data['house_id'])
    await message.answer('Объект успешно отредактирован', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Reports.url)
async def redact_reports(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    await rq.update_object(3, data['url'], data['house_id'])
    await message.answer('Объект успешно отредактирован', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Agreement.url)
async def redact_agreement(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    await rq.update_object(4, data['url'], data['house_id'])
    await message.answer('Объект успешно отредактирован', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.callback_query(F.data.startswith('find_object_'))
async def ask_object(callback: CallbackQuery):
    await callback.message.edit_text('Города', reply_markup=await kb.all_cities(int(callback.data.split('_')[2])))


@router_admin.callback_query(F.data.startswith('city_'))
async def write_areas(callback: CallbackQuery):
    await callback.message.edit_text('Районы', reply_markup=await kb.all_areas(callback.data.split('_')[1],
                                                                               callback.data.split('_')[2]))


@router_admin.callback_query(F.data.startswith('area_'))
async def write_houses(callback: CallbackQuery):
    await callback.message.edit_text('Объекты', reply_markup=await kb.all_house(callback.data.split('_')[1],
                                                                                callback.data.split('_')[2]))


@router_admin.callback_query(F.data == 'to_main_admin')
async def to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    if data['last_msg']:
        last_msg = data['last_msg']
        await callback.message.chat.delete_message(last_msg)
    await state.clear()
