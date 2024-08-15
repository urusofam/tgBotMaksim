from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import os
from dotenv import load_dotenv
from admin.keyboards import admin_menu, find_menu, all_cities, find_arendator_menu, houses_arendator
from database.requests import get_user_by_name
from keyboards.keyboards import houses_menu


router_admin = Router()
load_dotenv()


class Find(StatesGroup):
    name = State()

class Arendator(StatesGroup):
    name = State()

class House(StatesGroup):
    city = State()
    area = State()
    adress = State()


@router_admin.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Добро пожаловать в админ панель', reply_markup=admin_menu)


@router_admin.message(F.text == 'Связаться с собственником')
async def ask_method(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=find_menu)


@router_admin.message(F.text == 'Оповещения собственников')
async def alerts(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Выберите способ', reply_markup=find_arendator_menu)


@router_admin.callback_query(F.data == 'find_fio_arendator')
async def ask_fio(callback : CallbackQuery, state : FSMContext):
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
        await message.answer('@' + arendator.username, reply_markup=admin_menu)
    else:
        await message.answer('Арендатор не найден', reply_markup=admin_menu)
    await state.clear()


@router_admin.message(Arendator.name)
async def choose_object(message: Message, state: FSMContext):
    person = await get_user_by_name(message.text)
    if person:
        await message.answer('Выберите его объект', reply_markup = await houses_arendator(person.tg_id))
    else:
        await message.answer('Арендатор не найден', reply_markup=admin_menu)
    await state.clear()


@router_admin.callback_query(F.data == 'find_object')
async def ask_object(callback : CallbackQuery):
    await callback.message.edit_text('Объекты', reply_markup=await all_cities())


@router_admin.callback_query(F.data == 'to_main_admin')
async def ask_object(callback : CallbackQuery):
    await callback.message.edit_text('Вы вернулись в админ панель')