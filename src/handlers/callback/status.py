from aiogram import F, types, Router

from src.keyboards import main_keyboard
from src.models import User, Site

router = Router()


@router.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    user = User.get(User.chat_id == callback.from_user.id)

    sites = Site.select().where(Site.user == user.chat_id)

    await callback.message.answer(
        text=f"Бот <b>{'не ' if not user.tracking else ''}отслеживает</b> работоспособность сайтов. "
             f"\nУказано сайтов: <b>{len(sites)}</b> из 10."
             f"\nПериодичность опросов: раз в <b>{user.period}</b> минут{'у' if user.period == 1 else ''}.",
        reply_markup=main_keyboard()
    )
