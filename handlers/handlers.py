from aiogram import F, Router 
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboards.keyboards as kb

router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup = kb.main_start)

# @router.message(Command('help'))
# async def cmd_help(message: Message):
#     await message.answer('Это команда /help')

@router.message(F.text == 'Ввести другой номер телефона')
async def ask_phone(message: Message, state: FSMContext):
    await state.set_state(Reg.number)
    await message.answer('Пожалуйста, введите номер телефона в формате +7...')

@router.message(F.contact)
async def write_contact(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number[1:])
    await state.set_state(Reg.name)
    await message.answer('Теперь введите своё ФИО')

@router.message(Reg.number)
async def write_contact(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(Reg.name)
    await message.answer('Теперь введите своё ФИО')

@router.message(Reg.name)
async def write_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f'{data["name"]}\n{data["number"]}', reply_markup = kb.main_menu)
    await state.clear()

@router.message(F.text == 'Задать вопрос')
async def ask_question(message: Message):
    await message.answer('ЛС')

@router.message(F.text == 'Мои объекты')
async def ask_question(message: Message):
    await message.answer('ЛС', reply_markup = await kb.houses_menu())