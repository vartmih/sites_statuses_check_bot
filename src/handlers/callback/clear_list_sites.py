from aiogram import F, types, Router

from src.keyboards import main_keyboard
from src.models import Site, User

router = Router()


@router.callback_query(F.data == "clear_sites")
async def clear_sites(callback: types.CallbackQuery):
    user = User.get(User.chat_id == callback.from_user.id)
    Site.delete().where(Site.user == user.chat_id).execute()

    await callback.message.answer(
        text="Список сайтов очищен.",
        reply_markup=main_keyboard()
    )
