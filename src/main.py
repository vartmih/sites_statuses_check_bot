import asyncio
import logging

import requests
from requests.exceptions import ConnectionError
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from src.commands import set_commands
from src.fsm import FSM
from src.settings import settings
from src.keyboards import main_keyboard, url_keyboard_factory
from src.models import database, User, Site
from src.utils import is_valid_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)-5s - %(levelname)-5s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="../bot.log",
    filemode="w",
)

bot = Bot(token=settings.TOKEN.get_secret_value())

dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    user = User.get_or_none(User.username == message.from_user.username)

    if not user:
        user = User.create(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            chat_id=message.chat.id
        )

    if user.chat_id != message.chat.id:
        user.update(chat_id=message.chat.id).execute()

    await message.answer(
        text="Вас приветствует бот-помощник, который будет уведомлять "
             "Вас о работоспособности одного или нескольких сайтов, которые Вы ему укажите."
             "\nЧего желаете?",
        reply_markup=main_keyboard.as_markup()
    )


@dp.message(Command(commands=["menu"]))
async def menu_command(message: types.Message):
    await message.answer(
        text="Вы в главном меню. Чего желаете?",
        reply_markup=main_keyboard.as_markup()
    )


@dp.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Вы в главном меню. Чего желаете?",
        reply_markup=main_keyboard.as_markup()
    )


@dp.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    sites = Site.select().where(Site.user == callback.from_user.username)

    word = 'сайт'
    if 1 < len(sites) < 5:
        word += 'a'
    elif len(sites) >= 5 or len(sites) == 0:
        word += 'ов'

    await callback.message.answer(
        text=f"Бот {'не ' if not user.tracking else ''}отслеживает работоспособность сайтов. "
             f"\nВы указали {len(sites)} {word} из 10.",
        reply_markup=main_keyboard.as_markup()
    )


@dp.callback_query(F.data == "get_sites")
async def get_sites(callback: types.CallbackQuery):
    sites_query = Site.select().where(Site.user == callback.from_user.username)
    sites = [site.url for site in sites_query]
    if not sites:
        await callback.message.answer(
            text="Список сайтов пуст.",
            reply_markup=main_keyboard.as_markup()
        )
    else:
        await callback.message.answer(
            "Список сайтов ({0} из 10):\n{1}".format(len(sites), '\n'.join(sites)),
            reply_markup=main_keyboard.as_markup()
        )


@dp.callback_query(F.data == "clear_sites")
async def clear_sites(callback: types.CallbackQuery):
    Site.delete().where(Site.user == callback.from_user.username).execute()

    await callback.message.answer(
        text="Список сайтов очищен.",
        reply_markup=main_keyboard.as_markup()
    )


@dp.callback_query(F.data == "add_site")
async def add_site(callback: types.CallbackQuery, state: FSMContext):
    sites = Site.select().where(Site.user == callback.from_user.username)
    if len(sites) >= 10:
        await callback.message.answer(
            text="Вы отслеживаете максимально допустимое количество сайтов (10). "
                 "Удалите что-нибудь, чтобы добавить новые.",
            reply_markup=main_keyboard.as_markup()
        )
    else:
        await callback.message.answer('Введите ссылку на сайт:')
        await state.set_state(FSM.site)


@dp.callback_query(F.data == "delete_site")
async def delete_site_menu(callback: types.CallbackQuery):
    sites_query = Site.select().where(Site.user == callback.from_user.username)
    sites = [site.url for site in sites_query]
    if not sites:
        await callback.message.answer(
            text="Список сайтов пуст.",
            reply_markup=main_keyboard.as_markup()
        )
    else:
        keyboard = url_keyboard_factory(sites)
        await callback.message.answer(
            "Выберите сайт для удаления:",
            reply_markup=keyboard.as_markup()
        )


@dp.callback_query(F.data.startswith("delete_site"))
async def delete_site(callback: types.CallbackQuery):
    site = callback.data.split('_')[-1]

    Site.delete().where(Site.user == callback.from_user.username and Site.url == site).execute()
    sites = Site.select().where(Site.user == callback.from_user.username)

    await callback.message.answer(
        text=f"Сайт удален из отслеживаемых. Всего сайтов {len(sites)} из 10.",
        reply_markup=main_keyboard.as_markup()
    )


@dp.message(FSM.site)
async def save_site(message: types.Message, state: FSMContext):
    url_site = message.text
    is_valid = is_valid_url(url_site)
    if is_valid:
        Site.create(url=url_site, user=message.from_user.username)

        await state.clear()
        await message.answer(
            text="Сайт добавлен.",
            reply_markup=main_keyboard.as_markup()
        )
    else:
        await message.answer(
            text="Ссылка некорректна. "
                 "Пожалуйста, введите корректную ссылку.",
            reply_markup=main_keyboard.as_markup()
        )


@dp.message()
async def unknown(message: types.Message):
    await message.answer(
        text="Неизвестная команда. "
             "Выберите что-то из списка ниже.",
        reply_markup=main_keyboard.as_markup()
    )


@dp.callback_query(F.data == "run")
async def run(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)

    if user.tracking:
        await callback.message.answer(
            text="Бот уже отслеживает работоспособность сайтов. "
                 "\nЧто-нибудь еще?",
            reply_markup=main_keyboard.as_markup()
        )
    else:
        user.update(tracking=True).execute()
        await callback.message.answer(
            text="Бот начал отслеживать работоспособность сайтов. "
                 "\nЧто-нибудь еще?",
            reply_markup=main_keyboard.as_markup()
        )
        await run_sites_tracking(callback.message)


@dp.callback_query(F.data == "stop")
async def stop(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    user.update(tracking=False).execute()

    await callback.message.answer(
        text="Бот закончил отслеживать работоспособность сайтов. "
             "\nЧто-нибудь еще?",
        reply_markup=main_keyboard.as_markup()
    )


async def run_sites_tracking(message: types.Message | None = None, username: str | None = None):
    while True:
        tg_username = username or message.chat.username
        user = User.get(User.username == tg_username)

        if not user.tracking:
            break

        sites_query = Site.select().where(Site.user == tg_username)
        sites = [site.url for site in sites_query]

        for site in sites:
            try:
                response = requests.get(url=site, timeout=5)
                if response.status_code != 200:
                    raise ConnectionError
            except Exception as error:
                logging.info(f"Сайт {site} недоступен.")
                logging.error(error)
                if message:
                    await message.answer(text=f"Сайт {site} недоступен.")
                else:
                    await bot.send_message(chat_id=user.chat_id, text=f"Сайт {site} недоступен.")
        await asyncio.sleep(60)


async def main():
    with database:
        database.create_tables([User, Site])

    users_query = User.select()
    users = [user.username for user in users_query if user.tracking]

    for user in users:
        asyncio.create_task(run_sites_tracking(username=user))

    try:
        await set_commands(bot)
        await dp.start_polling(bot)
        logging.info("Бот запущен.")
    finally:
        logging.critical("Бот остановлен.")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
