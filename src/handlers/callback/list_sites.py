from aiogram import F, types, Router

from src.keyboards import main_keyboard
from src.models import Site

router = Router()


@router.callback_query(F.data == "get_sites")
async def get_sites(callback: types.CallbackQuery):
    sites_query = Site.select().where(Site.user == callback.from_user.username)
    sites = [site.url for site in sites_query]
    if not sites:
        await callback.message.answer(
            text="Список сайтов пуст.",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            "Список сайтов (<b>{0}</b> из 10):\n{1}".format(len(sites), '\n'.join(sites)),
            reply_markup=main_keyboard(),
            parse_mode='HTML'
        )
