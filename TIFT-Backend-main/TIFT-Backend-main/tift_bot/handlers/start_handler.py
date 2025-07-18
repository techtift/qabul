from aiogram import F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from tift_bot.dispatcher import dp
from tift_bot.buttons.reply import language_btn, menu
from tift_bot.buttons.text import *
from tift_bot.handlers.registration_handler import user_number_ask
from tift_bot.state.LoginState import AskInfo
from tift_bot.state.MenuState import MenuState
from tift_bot.state.LanguageState import LanguageState
from user.models.user import User


@dp.message(Command("language"), StateFilter(None))
async def language(message: Message, state: FSMContext) -> None:
    await state.set_state(LanguageState.language)
    await select_language_message(message, state)
    return


@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    await state.update_data(tg_id=tg_id)
    user, created = User.objects.get_or_create(tg_id=tg_id)
    if user.lang and user.is_verified and user.registered_by_bot:
        await state.update_data(lang=user.lang)
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return

    if user.lang:
        await state.update_data(lang=user.lang)
        await state.set_state(AskInfo.ask_number)
        await user_number_ask(message, state)
        return

    await message.answer(
        text=all.get("lang_choice"),
        reply_markup=language_btn()
    )
    await state.set_state(LanguageState.language)
    return


@dp.message(StateFilter(LanguageState.language))
async def select_language_message(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    await state.update_data(tg_id=tg_id)
    if message.text == uz_text:
        User.objects.update_or_create(
            tg_id=tg_id, defaults={'lang': 'uz'}
        )
        await state.update_data(lang='uz')
    elif message.text == ru_text:
        User.objects.update_or_create(
            tg_id=tg_id, defaults={'lang': 'ru'}
        )
        await state.update_data(lang='ru')
    else:
        await message.answer(
            text=all.get("lang_choice"),
            reply_markup=language_btn()
        )
        return
    user = User.objects.filter(tg_id=tg_id).first()
    if user.is_verified and user.registered_by_bot:
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    await state.set_state(AskInfo.ask_number)
    await user_number_ask(message, state)
    return



@dp.message(StateFilter(MenuState.menu))
async def menu_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang')
    tg_id=data.get('tg_id')
    user = User.objects.filter(tg_id=tg_id).first()
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('main_menu')"),
            reply_markup=menu(user.id,lang)
        )
    await state.set_state(None)



@dp.message(StateFilter(None), lambda message: message.text in (nazad, ortga))
async def to_back(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    await state.update_data(tg_id=tg_id)
    await message.delete()
    await state.set_state(MenuState.menu)
    await menu_handler(message, state)
    return


@dp.callback_query(StateFilter(None), F.data == "back")
async def back_to_menu(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.delete()
    await state.set_state(MenuState.menu)
    await menu_handler(callback_query.message, state)
    return





@dp.message(lambda message: message.text in ('💤 Выйти из аккаунта','💤 Hisobdan chiqish'))
async def exit(message: Message, state: FSMContext) -> None:
    data=await state.get_data()
    tg_id = data.get('tg_id')
    user = User.objects.filter(tg_id=tg_id).first()
    user.registered_by_bot = False
    user.lang = None
    user.tg_id=None
    user.save()
    await message.answer(text="To start conversation again 👉 /start",reply_markup=ReplyKeyboardRemove())
    await state.clear()
    return