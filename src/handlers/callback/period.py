from aiogram import F, types, Router

from src.keyboards import cron_keyboard, main_keyboard
from src.models import User

router = Router()


@router.callback_query(F.data == "period")
async def period(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Выберите период отслеживания:",
        reply_markup=cron_keyboard()
    )


@router.callback_query(F.data.startswith("period_"))
async def set_period(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    user.update(period=callback.data.split('_')[1]).execute()
    await callback.message.answer(
        text="Период отслеживания установлен. "
             "\nЧто-нибудь еще?",
        reply_markup=main_keyboard()
    )
