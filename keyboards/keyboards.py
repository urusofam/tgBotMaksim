from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import admins

from database.requests import get_houses, get_house_info

main_start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить номер из Telegram', request_contact=True)],
    [KeyboardButton(text='Ввести другой номер телефона')]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите пункт меню.')

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мои объекты')],
    [KeyboardButton(text='Задать вопрос')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')


admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить объект')],
    [KeyboardButton(text='Редактировать объект')],
    [KeyboardButton(text='Оповещения собственникам')],
    [KeyboardButton(text='Связаться с собственником')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

def is_admin(user_id):
    return user_id in admins
async def send_main_menu(message):
    if is_admin(message.from_user.id):
        await message.answer("Выберите действие:", reply_markup=admin_menu)
    else:
        await message.answer("Выберите действие:", reply_markup=main_menu)

async def houses_menu(tg_id):
    all_houses = await get_houses(tg_id)
    keyboard = InlineKeyboardBuilder()
    for house in all_houses:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"house_{house.id}"))
    return keyboard.adjust(2).as_markup()


async def houses_info_menu(house_id):
    all_info = await get_house_info(house_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отзывы', url=all_info.reviews))
    keyboard.add(InlineKeyboardButton(text='Гости', url=all_info.guests))
    keyboard.add(InlineKeyboardButton(text='Бронирование', url=all_info.book))
    keyboard.add(InlineKeyboardButton(text='Отчёты', url=all_info.reports))
    keyboard.add(InlineKeyboardButton(text='Мой договор', url=all_info.agreement))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data="to_main"))
    return keyboard.adjust(2).as_markup()
