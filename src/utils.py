import asyncio
import logging
from urllib.parse import urlparse

import requests
from aiogram import types, Bot
from requests import RequestException

from src.models import User, Site


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def run_sites_tracking(message: types.Message | None = None, username: str | None = None, bot: Bot | None = None):
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


async def restart_sites_tracking_for_all_active_users(bot: Bot):
    users_query = User.select()
    users = [user.username for user in users_query if user.tracking]

    for user in users:
        asyncio.create_task(run_sites_tracking(username=user, bot=bot))
