from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import all_houses, get_houses, all_houses_by_city, all_houses_by_areas

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить объект')],
    [KeyboardButton(text='Редактировать объект')],
    [KeyboardButton(text='Оповещения собственников')],
    [KeyboardButton(text='Связаться с собственником')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

cities_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Санкт-Петербург', callback_data='spb')],
    [InlineKeyboardButton(text='Другой', callback_data='another')]
])

back_out = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='to_main_admin')]
])


async def find_menu(choice):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Поиск по ФИО', callback_data=f'find_fio_{choice}')],
        [InlineKeyboardButton(text='Поиск по объектам', callback_data=f'find_object_{choice}')],
        [InlineKeyboardButton(text='Отмена', callback_data='to_main_admin')]
    ])
    return keyboard


async def confirm_menu(house_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтверждаю', callback_data=f'confirm_delete_{house_id}')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel_delete')]
    ])
    return keyboard


async def houses_info_menu_admin(house_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=
                                    [[InlineKeyboardButton(text='Отзывы', callback_data=f'redact_reviews_{house_id}')],
                                     [InlineKeyboardButton(text='Гости', callback_data=f'redact_guests_{house_id}')],
                                     [InlineKeyboardButton(text='Бронирование',
                                                           callback_data=f'redact_book_{house_id}')],
                                     [InlineKeyboardButton(text='Отчёты', callback_data=f'redact_reports_{house_id}')],
                                     [InlineKeyboardButton(text='Мой договор',
                                                           callback_data=f'redact_agreement_{house_id}')],
                                     [InlineKeyboardButton(text='Удалить объект',
                                                           callback_data=f'redact_delete_{house_id}')],
                                     [InlineKeyboardButton(text='Отмена', callback_data="to_main_admin")]
                                     ])
    return keyboard


async def all_cities(choice):
    all_city = await all_houses()
    cities = []
    keyboard = InlineKeyboardBuilder()
    for house in all_city:
        if house.city not in cities:
            keyboard.add(InlineKeyboardButton(text=house.city, callback_data=f"city_{choice}_{house.city}"))
            cities.append(house.city)
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_areas(choice, city):
    all_area = await all_houses_by_city(city)
    areas = []
    keyboard = InlineKeyboardBuilder()
    for house in all_area:
        if house.area not in areas:
            keyboard.add(InlineKeyboardButton(text=house.area, callback_data=f"area_{choice}_{house.area}"))
            areas.append(house.area)
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='to_main_admin'))
    return keyboard.adjust(2).as_markup()


async def all_house(choice, area):
    full_house = await all_houses_by_areas(area)
    keyboard = InlineKeyboardBuilder()
    for house in full_house:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{choice}_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='to_main_admin'))
    return keyboard.adjust(1).as_markup()


async def houses_arendator(choice, tg_id):
    all_houses_arenda = await get_houses(tg_id)
    keyboard = InlineKeyboardBuilder()
    for house in all_houses_arenda:
        keyboard.add(InlineKeyboardButton(text=house.adress, callback_data=f"arendator_house_{choice}_{house.id}"))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='to_main_admin'))
    return keyboard.adjust(1).as_markup()


async def reports(house_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Новый объект', callback_data=f'report_obj_{house_id}')],
        [InlineKeyboardButton(text='Гости', callback_data=f'report_guests_{house_id}')],
        [InlineKeyboardButton(text='Бронь', callback_data=f'report_bron_{house_id}')],
        [InlineKeyboardButton(text='Отчёты', callback_data=f'report_reports_{house_id}')],
        [InlineKeyboardButton(text='Отзывы', callback_data=f'report_reviews_{house_id}')],
        [InlineKeyboardButton(text='Договор', callback_data=f'report_agreement_{house_id}')],
        [InlineKeyboardButton(text='Другое', callback_data=f'report_other_{house_id}')],
        [InlineKeyboardButton(text='Отмена', callback_data='to_main_admin')]
    ])
    return keyboard
