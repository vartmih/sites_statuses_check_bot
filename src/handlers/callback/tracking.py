from aiogram import F, types, Router

from src import utils
from src.keyboards import main_keyboard
from src.models import User, Site

router = Router()


@router.callback_query(F.data == "run")
async def run(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    sites = Site.select().where(Site.user == callback.from_user.username)

    if user.tracking:
        await callback.message.answer(
            text="Бот уже отслеживает работоспособность сайтов. "
                 "\nЧто-нибудь еще?",
            reply_markup=main_keyboard()
        )
    elif sites:
        user.update(tracking=True).execute()
        await callback.message.answer(
            text="Бот начал отслеживать работоспособность сайтов. "
                 "\nЧто-нибудь еще?",
            reply_markup=main_keyboard().as_markup()
        )
        await utils.run_sites_tracking(callback.message)
    else:
        await callback.message.answer(
            text="Список сайтов пуст. Добавьте хотя бы один сайт."
                 "\nЧто-нибудь еще?",
            reply_markup=main_keyboard()
        )


@router.callback_query(F.data == "stop")
async def stop(callback: types.CallbackQuery):
    user = User.get(User.username == callback.from_user.username)
    user.update(tracking=False).execute()

    await callback.message.answer(
        text="Бот закончил отслеживать работоспособность сайтов. "
             "\nЧто-нибудь еще?",
        reply_markup=main_keyboard().as_markup()
    )
