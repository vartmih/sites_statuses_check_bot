from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from src import utils
from src.fsm import FSM
from src.keyboards import main_keyboard
from src.models import Site

router = Router()


@router.message(FSM.site)
async def save_url(message: types.Message, state: FSMContext):
    url_site = message.text
    is_valid = utils.is_valid_url(url_site)
    if is_valid:
        Site.create(url=url_site, user=message.from_user.username)

        await state.clear()
        await message.answer(
            text="Сайт добавлен.",
            reply_markup=main_keyboard()
        )
    else:
        await message.answer(
            text="Ссылка некорректна. "
                 "Пожалуйста, введите корректную ссылку.",
            reply_markup=main_keyboard()
        )
