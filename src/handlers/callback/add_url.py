from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from src.fsm import FSM
from src.keyboards import main_keyboard
from src.models import Site

router = Router()


@router.callback_query(F.data == "add_site")
async def add_site(callback: types.CallbackQuery, state: FSMContext):
    sites = Site.select().where(Site.user == callback.from_user.username)
    if len(sites) >= 10:
        await callback.message.answer(
            text="Вы отслеживаете максимально допустимое количество сайтов (10). "
                 "Удалите что-нибудь, чтобы добавить новые.",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer('Введите ссылку на сайт:')
        await state.set_state(FSM.site)
