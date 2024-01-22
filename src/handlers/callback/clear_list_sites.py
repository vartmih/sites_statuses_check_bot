from aiogram import F, types, Router

from src.keyboards import main_keyboard
from src.models import Site

router = Router()


@router.callback_query(F.data == "clear_sites")
async def clear_sites(callback: types.CallbackQuery):
    Site.delete().where(Site.user == callback.from_user.username).execute()

    await callback.message.answer(
        text="Список сайтов очищен.",
        reply_markup=main_keyboard()
    )
