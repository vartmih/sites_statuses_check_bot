from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

main_keyboard = InlineKeyboardBuilder()

main_keyboard.add(InlineKeyboardButton(text="✅Начать отслеживание", callback_data="run"))
main_keyboard.add(InlineKeyboardButton(text="🚫Остановить отслеживание", callback_data="stop"))
main_keyboard.add(InlineKeyboardButton(text="➕Добавить сайт", callback_data="add_site"))
main_keyboard.add(InlineKeyboardButton(text="➖Удалить сайт", callback_data="delete_site"))
main_keyboard.add(InlineKeyboardButton(text="🗂️Список сайтов", callback_data="get_sites"))
main_keyboard.add(InlineKeyboardButton(text="🗑️Очистить список", callback_data="clear_sites"))
main_keyboard.add(InlineKeyboardButton(text="ℹ️Статус", callback_data="status"))

main_keyboard.adjust(1, 1, 2, 2)


def url_keyboard_factory(sites: list[str]) -> InlineKeyboardBuilder:
    url_keyboard = InlineKeyboardBuilder()
    for site in sites:
        url_keyboard.add(InlineKeyboardButton(text=f'👉🏼 {site}', callback_data=f'delete_site_{site}'))

    url_keyboard.add(InlineKeyboardButton(text="❌Отмена", callback_data="menu"))
    url_keyboard.adjust(1)
    return url_keyboard
