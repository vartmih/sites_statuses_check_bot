import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src import utils
from src.commands import set_commands
from src.handlers.callback import add_url, delete_url, clear_list_sites, list_sites, status, period, menu, tracking
from src.handlers.message import save_url, command_start, command_menu, unknown_command
from src.models import database, User, Site
from src.settings import settings


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    await bot.set_webhook(
        url=f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET.get_secret_value()
    )


def main():
    with database:
        database.create_tables([User, Site])
    bot = Bot(token=settings.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_routers(save_url.router, command_start.router, command_menu.router, unknown_command.router)
    dp.include_routers(add_url.router, delete_url.router, clear_list_sites.router, list_sites.router,
                       status.router, period.router, menu.router, tracking.router)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET.get_secret_value(),
    )

    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)
    utils.restart_sites_tracking_for_all_active_users(bot=bot)
    logging.info("Бот запущен.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)-5s - %(levelname)-5s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="../bot.log",
        filemode="w",
    )
    main()
