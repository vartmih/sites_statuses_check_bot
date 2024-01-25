from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from src.fsm import FSM
from src.keyboards import main_keyboard
from src.models import Site, User

router = Router()


@router.callback_query(F.data == "add_site")
async def add_site(callback: types.CallbackQuery, state: FSMContext):
    user = User.get(User.chat_id == callback.from_user.id)

    sites = Site.select().where(Site.user == user.chat_id)

    if len(sites) >= 10:
        await callback.message.answer(
            text="Вы отслеживаете максимально допустимое количество сайтов (<b>10</b>). "
                 "Удалите что-нибудь, чтобы добавить новые.",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            text="Пример формата ссылки: <code>https://example.com</code>.\n"
                 "Введите ссылку на сайт:"
        )
        await state.set_state(FSM.site)
