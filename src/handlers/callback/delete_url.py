from aiogram import F, types, Router

from src.keyboards import main_keyboard, url_keyboard_factory
from src.models import Site

router = Router()


@router.callback_query(F.data == "delete_site")
async def delete_url_menu(callback: types.CallbackQuery):
    sites_query = Site.select().where(Site.user == callback.from_user.username)
    sites = [site.url for site in sites_query]
    if not sites:
        await callback.message.answer(
            text="Список сайтов пуст.",
            reply_markup=main_keyboard().as_markup()
        )
    else:
        keyboard = url_keyboard_factory(sites)
        await callback.message.answer(
            "Выберите сайт для удаления:",
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith("delete_site"))
async def delete_url(callback: types.CallbackQuery):
    site = callback.data.split('_')[-1]

    Site.delete().where(Site.user == callback.from_user.username and Site.url == site).execute()
    sites = Site.select().where(Site.user == callback.from_user.username)

    await callback.message.answer(
        text=f"Сайт удален из отслеживаемых. Всего сайтов <b>{len(sites)}</b> из 10.",
        reply_markup=main_keyboard()
    )
