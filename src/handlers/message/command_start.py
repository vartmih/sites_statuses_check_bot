from aiogram import types, Router
from aiogram.filters import Command

from src.keyboards import main_keyboard
from src.models import User

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    user = User.get_or_none(User.username == message.from_user.username)

    if not user:
        user = User.create(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            chat_id=message.chat.id
        )

    if user.chat_id != message.chat.id:
        user.update(chat_id=message.chat.id).execute()

    await message.answer(
        text="Вас приветствует бот-помощник, который будет уведомлять "
             "Вас о работоспособности одного или нескольких сайтов, которые Вы ему укажите."
             "\nЧего желаете?",
        reply_markup=main_keyboard()
    )
