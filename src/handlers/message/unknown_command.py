from aiogram import types, Router

from src.keyboards import main_keyboard

router = Router()


@router.message()
async def unknown(message: types.Message):
    await message.answer(
        text="Неизвестная команда. "
             "Выберите что-то из списка ниже.",
        reply_markup=main_keyboard()
    )
