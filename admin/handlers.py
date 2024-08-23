from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage

import os
from dotenv import load_dotenv
import admin.keyboards as kb
from database.requests import get_user_by_name, get_house_info, get_user_by_tg_id, add_object

router_admin = Router()
load_dotenv()


class Find(StatesGroup):
    name = State()

class Add(StatesGroup):
    name = State()
    city = State()
    area = State()
    adress = State()

class Arendator(StatesGroup):
    name = State()


class House(StatesGroup):
    city = State()
    area = State()
    adress = State()


@router_admin.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Добро пожаловать в админ панель', reply_markup=kb.admin_menu)


@router_admin.message(F.text == 'Связаться с собственником')
async def ask_method(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=kb.find_menu)


@router_admin.message(F.text == 'Добавить объект')
async def add_object_arendator(message: Message, state : FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.set_state(Add.name)
        await message.answer('Введите ФИО собственника')


@router_admin.message(Add.name)
async def ask_add_name(message: Message, state: FSMContext):
    arendator = await get_user_by_name(message.text)
    if arendator:
        await state.update_data(name = arendator.tg_id)
        await message.answer('Выберите город', reply_markup=kb.cities_menu)
    else:
        await state.clear()
        await message.answer('Собственник не найден')


@router_admin.callback_query(F.data == 'spb')
async def ask_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(city = 'Санкт-Петербург')
    await callback.message.edit_text('Введите район', reply_markup=kb.back_out)
    await state.set_state(Add.area)


@router_admin.callback_query(F.data == 'another')
async def ask_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите город', reply_markup=kb.back_out)
    await state.set_state(Add.city)


@router_admin.message(Add.city)
async def ask_add_city(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    await message.answer('Введите район', reply_markup=kb.back_out)
    await state.set_state(Add.area)


@router_admin.message(Add.area)
async def ask_add_area(message: Message, state: FSMContext):
    await state.update_data(area = message.text)
    await message.answer('Введите адрес', reply_markup=kb.back_out)
    await state.set_state(Add.adress)


@router_admin.message(Add.adress)
async def write_object(message: Message, state: FSMContext):
    await state.update_data(adress = message.text)
    data = await state.get_data()
    print(data['name'], data['city'], data['area'], data['adress'])
    await add_object(data['name'], data['city'], data['area'], data['adress'])
    await message.answer(f"{data['name']}\n{data['city']}\n{data['area']}\n{data['adress']}", reply_markup=kb.admin_menu)
    await state.clear()



@router_admin.message(F.text == 'Оповещения собственников')
async def alerts(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=kb.find_arendator_menu)


@router_admin.callback_query(F.data == 'find_fio_arendator')
async def fio_ask(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Arendator.name)
    await callback.message.delete()
    await callback.message.answer('Введите ФИО')


@router_admin.callback_query(F.data == 'find_fio')
async def ask_fio(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Find.name)
    await callback.message.delete()
    await callback.message.answer('Введите ФИО')


@router_admin.message(Find.name)
async def write_to_user(message: Message, state: FSMContext):
    arendator = await get_user_by_name(message.text)
    if arendator:
        await message.answer('@' + arendator.username, reply_markup=kb.admin_menu)
    else:
        await message.answer('Арендатор не найден', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.message(Arendator.name)
async def choose_object(message: Message, state: FSMContext):
    person = await get_user_by_name(message.text)
    if person:
        await message.answer('Выберите его объект', reply_markup=await kb.houses_arendator(person.tg_id))
    else:
        await message.answer('Арендатор не найден', reply_markup=kb.admin_menu)
    await state.clear()


@router_admin.callback_query(F.data.startswith('arendator_house'))
async def house_arendator(callback: CallbackQuery):
    await callback.message.edit_text('Выберите что вам нужно',
                                     reply_markup=await kb.reports(callback.data.split('_')[2]))


@router_admin.callback_query(F.data == 'find_object')
async def ask_object(callback: CallbackQuery):
    await callback.message.edit_text('Города', reply_markup=await kb.cities_all())


@router_admin.callback_query(F.data == 'find_object_arendator')
async def object_ask(callback: CallbackQuery):
    await callback.message.edit_text('Города', reply_markup=await kb.all_cities())


@router_admin.callback_query(F.data.startswith('city_'))
async def write_areas(callback: CallbackQuery):
    await callback.message.edit_text('Районы', reply_markup=await kb.all_areas(callback.data.split('_')[1]))


@router_admin.callback_query(F.data.startswith('area_'))
async def write_houses(callback: CallbackQuery):
    await callback.message.edit_text('Объекты', reply_markup=await kb.all_house(callback.data.split('_')[1]))


@router_admin.callback_query(F.data.startswith('cities_'))
async def write_areas(callback: CallbackQuery):
    await callback.message.edit_text('Районы', reply_markup=await kb.areas_all(callback.data.split('_')[1]))


@router_admin.callback_query(F.data.startswith('areas_'))
async def write_houses(callback: CallbackQuery):
    await callback.message.edit_text('Объекты', reply_markup=await kb.house_all(callback.data.split('_')[1]))


@router_admin.callback_query(F.data.startswith('username_house_'))
async def write_to_arendator(callback: CallbackQuery):
    house = await get_house_info(callback.data.split('_')[2])
    arendator = await get_user_by_tg_id(house.arendator)
    if arendator:
        await callback.message.edit_text('@' + arendator.username)
    else:
        await callback.message.edit_text('Арендатор не найден')



@router_admin.callback_query(F.data == 'to_main_admin')
async def to_main(callback: CallbackQuery):
    await callback.message.edit_text('Вы вернулись в админ панель')
