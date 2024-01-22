from aiogram import types, Router
from aiogram.filters import Command

from src.keyboards import main_keyboard

router = Router()


@router.message(Command(commands=["menu"]))
async def menu_command(message: types.Message):
    await message.answer(
        text="Вы в главном меню. Чего желаете?",
        reply_markup=main_keyboard()
    )
