from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboards.keyboards as kb
import database.requests as rq

router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бота по субаренде! Пройдите регистарцию!', reply_markup = kb.main_start)

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
    await rq.add_user(message.from_user.id, data['name'], data['number'])
    await message.answer(f'{data["name"]}\n{data["number"]}', reply_markup = kb.main_menu)
    await state.clear()

@router.message(F.text == 'Задать вопрос')
async def ask_question(message: Message):
    await message.answer('Ссылка на Максима')

@router.callback_query(F.data == "to_main")
async def to_main(callback : CallbackQuery):
    await callback.answer('Вы вернулись на главную')
    await callback.message.edit_text('Ваши объекты', reply_markup=await kb.houses_menu(callback.from_user.id))
    print(callback.message.from_user.id)

@router.callback_query(F.data.startswith('house_'))
async def house(callback: CallbackQuery):
    await callback.answer('Вы выбрали дом')
    await callback.message.edit_text('Выберите что вам нужно', reply_markup= await kb.houses_info_menu(callback.data.split('_')[1]))

@router.message(F.text == 'Мои объекты')
async def write_houses(message: Message):
    await message.answer('Ваши объекты', reply_markup = await kb.houses_menu(message.from_user.id))