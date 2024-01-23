import asyncio
import logging

from aiogram import Bot, Dispatcher

from src import utils
from src.commands import set_commands
from src.handlers.callback import add_url, delete_url, clear_list_sites, list_sites, status, period, menu, tracking
from src.handlers.message import save_url, command_start, command_menu, unknown_command
from src.models import database, User, Site
from src.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)-5s - %(levelname)-5s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="../bot.log",
    filemode="w",
)

bot = Bot(token=settings.TOKEN.get_secret_value())

dp = Dispatcher()


async def main():
    with database:
        database.create_tables([User, Site])

    users_query = User.select()
    users = [user.username for user in users_query if user.tracking]

    for user in users:
        asyncio.create_task(utils.run_sites_tracking(username=user))

    try:
        dp.include_routers(save_url.router, command_start.router, command_menu.router, unknown_command.router)
        dp.include_routers(add_url.router, delete_url.router, clear_list_sites.router, list_sites.router,
                           status.router, period.router, menu.router, tracking.router)
        await set_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, skip_updates=True)
        logging.info("Бот запущен.")
    finally:
        logging.critical("Бот остановлен.")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
