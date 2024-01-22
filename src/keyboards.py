from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="✅Начать отслеживание", callback_data="run"))
    keyboard.add(InlineKeyboardButton(text="🚫Остановить отслеживание", callback_data="stop"))
    keyboard.add(InlineKeyboardButton(text="🕒️Периодичность опроса", callback_data="period"))
    keyboard.add(InlineKeyboardButton(text="➕Добавить сайт", callback_data="add_site"))
    keyboard.add(InlineKeyboardButton(text="➖Удалить сайт", callback_data="delete_site"))
    keyboard.add(InlineKeyboardButton(text="🗂️Список сайтов", callback_data="get_sites"))
    keyboard.add(InlineKeyboardButton(text="🗑️Очистить список", callback_data="clear_sites"))
    keyboard.add(InlineKeyboardButton(text="ℹ️Статус", callback_data="status"))

    keyboard.adjust(1, 1, 1, 2, 2)
    return keyboard.as_markup()


def url_keyboard_factory(sites: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for site in sites:
        keyboard.add(InlineKeyboardButton(text=f'👉🏼 {site}', callback_data=f'delete_site_{site}'))

    keyboard.add(InlineKeyboardButton(text="❌Отмена", callback_data="menu"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def cron_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    minutes = (1, 5, 10, 15, 30, 60)

    for time in minutes:
        keyboard.add(
            InlineKeyboardButton(text=f"{time} минут{'а' if time == 1 else ''}", callback_data=f"period_{time}_minute")
        )

    keyboard.add(InlineKeyboardButton(text="❌Отмена", callback_data="menu"))
    keyboard.adjust(2)
    return keyboard.as_markup()
