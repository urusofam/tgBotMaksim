from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import all_houses, get_houses, all_houses_by_city, all_houses_by_areas, get_house_info

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить объект')],
    [KeyboardButton(text='Редактировать объект')],
    [KeyboardButton(text='Оповещения собственников')],
    [KeyboardButton(text='Связаться с собственником')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

find_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск по ФИО', callback_data='find_fio')],
    [InlineKeyboardButton(text='Поиск по объектам', callback_data='find_object')],
    [InlineKeyboardButton(text='На главную', callback_data='to_main_admin')]
])

find_arendator_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск по ФИО', callback_data='find_fio_arendator')],
    [InlineKeyboardButton(text='Поиск по объектам', callback_data='find_object_arendator')],
    [InlineKeyboardButton(text='На главную', callback_data='to_main_admin')]
])

cities_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Санкт-Петербург', callback_data='spb')],
    [InlineKeyboardButton(text='Другой', callback_data='another')]
])

back_out = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На главную', callback_data='to_main_admin')]
])


async def houses_info_menu_admin(house_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отзывы', callback_data=f'redact_reviews_{house_id}'))
    keyboard.add(InlineKeyboardButton(text='Гости', callback_data=f'redact_guests_{house_id}'))
    keyboard.add(InlineKeyboardButton(text='Бронирование', callback_data=f'redact_book_{house_id}'))
    keyboard.add(InlineKeyboardButton(text='Отчёты', callback_data=f'redact_reports_{house_id}'))
    keyboard.add(InlineKeyboardButton(text='Мой договор', callback_data=f'redact_agreement_{house_id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data="to_main_admin"))
    return keyboard.adjust(2).as_markup()


async def all_cities(choice):
    all_city = await all_houses()
    cities = []
    keyboard = InlineKeyboardBuilder()
    for house in all_city:
        if house.city not in cities:
            keyboard.add(InlineKeyboardButton(text=house.city, callback_data=f"city_{choice}_{house.city}"))
            cities.append(house.city)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_areas(choice, city):
    all_area = await all_houses_by_city(city)
    areas = []
    keyboard = InlineKeyboardBuilder()
    for house in all_area:
        if house.area not in areas:
            keyboard.add(InlineKeyboardButton(text=house.area, callback_data=f"area_{choice}_{house.area}"))
            areas.append(house.area)
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_house(choice, area):
    full_house = await all_houses_by_areas(area)
    keyboard = InlineKeyboardBuilder()
    for house in full_house:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{choice}_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def houses_arendator(choice, tg_id):
    all_houses_arenda = await get_houses(tg_id)
    keyboard = InlineKeyboardBuilder()
    for house in all_houses_arenda:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{choice}_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def reports(house_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Гости', callback_data=f'report_guests_{house_id}')],
        [InlineKeyboardButton(text='Бронь', callback_data=f'report_bron_{house_id}')],
        [InlineKeyboardButton(text='Отчёты', callback_data=f'report_reports_{house_id}')],
        [InlineKeyboardButton(text='Отзывы', callback_data=f'report_reviews_{house_id}')],
        [InlineKeyboardButton(text='Договор', callback_data=f'report_agreement_{house_id}')],
        [InlineKeyboardButton(text='Другое', callback_data=f'report_other_{house_id}')],
        [InlineKeyboardButton(text='На главную', callback_data='to_main_admin')]
    ])
    return keyboard
