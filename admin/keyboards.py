from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import all_houses, get_houses

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить объект')],
    [KeyboardButton(text='Редактировать объект')],
    [KeyboardButton(text='Оповещения собственников')],
    [KeyboardButton(text='Связаться с собственником')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

find_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск по ФИО', callback_data = 'find_fio')],
    [InlineKeyboardButton(text='Поиск по объектам', callback_data = 'find_object')],
    [InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin')]
])

find_arendator_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск по ФИО', callback_data = 'find_fio_arendator')],
    [InlineKeyboardButton(text='Поиск по объектам', callback_data = 'find_object_arendator')],
    [InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin')]
])



async def all_cities():
    full_house = await all_houses()
    keyboard = InlineKeyboardBuilder()
    for house in full_house:
        keyboard.add(InlineKeyboardButton(text=house.city, callback_data=f"city_{house.city}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()

async def houses_arendator(tg_id):
    all_houses = await get_houses(tg_id)
    keyboard = InlineKeyboardBuilder()
    for house in all_houses:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"house_arendator_{house.id}"))
    return keyboard.adjust(2).as_markup()