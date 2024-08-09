from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import houses

main_start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Получить номер из Telegram', request_contact = True)],
    [KeyboardButton(text = 'Ввести другой номер телефона')]
], resize_keyboard = True, one_time_keyboard = True, input_field_placeholder = 'Выберите пункт меню.')

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Мои объекты')],
    [KeyboardButton(text = 'Задать вопрос')]
], resize_keyboard = True, input_field_placeholder = 'Выберите пункт меню.')

async def houses_menu():
    keyboard = ReplyKeyboardBuilder()
    for house in houses:
        keyboard.add(KeyboardButton(text=house))
    keyboard.add(KeyboardButton(text = "Назад"))
    return keyboard.adjust(2).as_markup()