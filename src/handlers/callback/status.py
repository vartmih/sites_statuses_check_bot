from aiogram import F, types, Router

from src.keyboards import main_keyboard
from src.models import User, Site

router = Router()


@router.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    sites = Site.select().where(Site.user == callback.from_user.username)

    await callback.message.answer(
        text=f"Бот {'не ' if not user.tracking else ''}отслеживает работоспособность сайтов. "
             f"\nУказано сайтов: {len(sites)} из 10."
             f"\nПериодичность опросов: раз в {user.period} минут{'у' if user.period == 1 else ''}.",
        reply_markup=main_keyboard()
    )
