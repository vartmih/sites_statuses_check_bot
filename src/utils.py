import asyncio
import logging
from urllib.parse import urlparse

import requests
from aiogram import types
from requests import RequestException

from src.main import bot
from src.models import User, Site


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


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
                    raise RequestException
            except RequestException:
                logging.info(f"Сайт {site} недоступен.")
                if message:
                    await message.answer(text=f"Сайт {site} недоступен.")
                else:
                    await bot.send_message(chat_id=user.chat_id, text=f"Сайт {site} недоступен.")
            except Exception as error:
                logging.error(error)

        await asyncio.sleep(user.period * 60)
