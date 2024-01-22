from aiogram import F, types, Router

from src.keyboards import main_keyboard

router = Router()


@router.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        text="Вы в главном меню. Чего желаете?",
        reply_markup=main_keyboard()
    )
