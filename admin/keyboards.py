from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import all_houses, get_houses, all_houses_by_city, all_houses_by_areas

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
    all_city = await all_houses()
    cities = []
    keyboard = InlineKeyboardBuilder()
    for house in all_city:
        if house.city not in cities:
            keyboard.add(InlineKeyboardButton(text=house.city, callback_data=f"city_{house.city}"))
            cities.append(house.city)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def cities_all():
    all_city = await all_houses()
    cities = []
    keyboard = InlineKeyboardBuilder()
    for house in all_city:
        if house.city not in cities:
            keyboard.add(InlineKeyboardButton(text=house.city, callback_data=f"cities_{house.city}"))
            cities.append(house.city)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_areas(city):
    all_area = await all_houses_by_city(city)
    areas = []
    keyboard = InlineKeyboardBuilder()
    for house in all_area:
        if house.area not in areas:
            keyboard.add(InlineKeyboardButton(text=house.area, callback_data=f"area_{house.area}"))
            areas.append(house.area)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def areas_all(city):
    all_area = await all_houses_by_city(city)
    areas = []
    keyboard = InlineKeyboardBuilder()
    for house in all_area:
        if house.area not in areas:
            keyboard.add(InlineKeyboardButton(text=house.area, callback_data=f"areas_{house.area}"))
            areas.append(house.area)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_house(area):
    full_house = await all_houses_by_areas(area)
    keyboard = InlineKeyboardBuilder()
    for house in full_house:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def house_all(area):
    full_house = await all_houses_by_areas(area)
    keyboard = InlineKeyboardBuilder()
    for house in full_house:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"username_house_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data = 'to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def houses_arendator(tg_id):
    all_houses = await get_houses(tg_id)
    keyboard = InlineKeyboardBuilder()
    for house in all_houses:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def reports(house_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Гости', callback_data=f'guests_{house_id}')],
        [InlineKeyboardButton(text='Бронь', callback_data=f'bron_{house_id}')],
        [InlineKeyboardButton(text='Отчёты', callback_data=f'reports_{house_id}')],
        [InlineKeyboardButton(text='Отзывы', callback_data=f'reviews_{house_id}')],
        [InlineKeyboardButton(text='Договор', callback_data=f'agreement_{house_id}')],
        [InlineKeyboardButton(text='Другое', callback_data=f'other_{house_id}')]
    ])
    return keyboard