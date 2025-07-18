import re
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from tift_bot.dispatcher import dp
from tift_bot.buttons.reply import get_contact_keyboard, back, reset_password
from tift_bot.buttons.text import *
from tift_bot.handlers.reset_password_handler import reset_password_handler
from tift_bot.state.LoginState import AskInfo
from tift_bot.state.MenuState import MenuState
from tift_bot.utils import format_phone_number
from user.models.user import User
from user.services.create_otp import create_otp_service,verify_otp
from tift_bot.utils import create_user_service_bot







@dp.message(StateFilter(AskInfo.ask_number))
async def user_number_ask(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    name = message.from_user.first_name
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('menu_text')").format(name=name),
            reply_markup=get_contact_keyboard(lang)
        )
    else:
        await message.answer(text=all.get("undefined_lang"))

    await state.set_state(AskInfo.get_number)
    return

@dp.message(StateFilter(AskInfo.get_number))
async def user_number_get(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    phone_number = None
    if message.contact:
        phone_number = format_phone_number(message.contact.phone_number)
    elif message.text and re.match(r"^\+\d{9,13}$", message.text):
        phone_number = format_phone_number(message.text)
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if phone_number:
        await state.update_data(phone_number=phone_number)
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.tg_id == message.from_user.id and user.registered_by_bot:
            await state.set_state(MenuState.menu)
            await menu_handler(message, state)
            return
        elif user and user.tg_id != message.from_user.id :
            if lang:
                await message.answer(text=eval(f"{lang}.get('ask_password')"), reply_markup=reset_password(lang))
            await state.set_state(AskInfo.ask_login)
            return

        try:
            response = create_otp_service(phone_number)
            if response.is_sent:
                if lang:
                    await message.answer(
                        text=eval(f"{lang}.get('enter_sms')"),
                        reply_markup=ReplyKeyboardRemove()
                    )
                await state.set_state(AskInfo.verify_number)
                return
        except Exception as e:
            if lang:
                print(e)
                await message.answer(
                text=eval(f"{lang}.get('enter_sms_error')"),
                reply_markup=get_contact_keyboard(lang)
            )
            await state.set_state(AskInfo.get_number)
            return
    else:
        await state.set_state(AskInfo.ask_number)
        await user_number_ask(message, state)

@dp.message(StateFilter(AskInfo.ask_login))
async def login(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang')
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in ( nazad, ortga):
        await state.set_state(AskInfo.ask_number)
        await user_number_ask(message, state)
        return
    if message.text in ("📟 Изменить пароль","📟 Parolni o'zgartirish"):
        await state.set_state(None)
        await reset_password_handler(message, state)
        return

    phone_number = data.get('phone_number')
    user = User.objects.filter(phone_number=phone_number).first()
    if not user.check_password(message.text):
        if lang:
            await message.answer(text=eval(f"{lang}.get('login_error')"), reply_markup=back(lang))
        await state.set_state(AskInfo.ask_login)
        await user_number_ask(message, state)
        return
    for deleted_user in User.objects.filter(tg_id=message.from_user.id):
        deleted_user.hard_delete()
    user.tg_id = message.from_user.id
    user.registered_by_bot = True
    data['phone_number'] = phone_number
    data['tg_id'] = message.from_user.id
    user.tg_id = message.from_user.id
    user.save()
    await state.update_data(data=data)
    await state.set_state(MenuState.menu)
    await menu_handler(message, state)
    return


@dp.message(StateFilter(AskInfo.verify_number))
async def user_number_verify(message: Message, state: FSMContext) -> None:
    otp = str(message.text)
    data = await state.get_data()
    phone_number = data.get("phone_number")
    lang = data.get("lang")
    user = User.objects.filter(tg_id=message.from_user.id).first()
    if not lang:
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if otp and phone_number:
        try:
            respone = verify_otp(phone_number, otp)
            if respone:

                if lang:
                    await message.answer(
                        text=eval(f"{lang}.get('password_text')"),
                        reply_markup=back(lang)
                    )
                await message.answer(text="🫣")
                await state.set_state(AskInfo.password)
                return
        except Exception as e:
            if lang:
                print(e)
                await message.answer(
                text=eval(f"{lang}.get('sms_wrong')"),
                reply_markup=get_contact_keyboard(lang)
            )
            await state.set_state(AskInfo.get_number)
            return



@dp.message(StateFilter(AskInfo.password))
async def password_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    await message.delete()
    if message.text in (nazad, ortga):
        await state.set_state(AskInfo.ask_number)
        await user_number_ask(message, state)
        return
    data['password'] = message.text
    await state.set_data(data)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('confirm_password_text')"),
            reply_markup=back(lang)
        )

    await state.set_state(AskInfo.verify_password)


@dp.message(StateFilter(AskInfo.verify_password))
async def verify_password_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    await message.delete()
    data = await state.get_data()
    lang = data.get("lang")
    tg_id=data.get('tg_id')
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (nazad, ortga):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('password_text')"),
                reply_markup=back(lang)
            )
        await message.answer(text="🫣")
        await state.set_state(AskInfo.password)
        return

    if not message.text == data.get("password"):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('confirm_error_text')"),
                reply_markup=back(lang)
            )
        await state.set_state(AskInfo.password)
        return
    create_user_service_bot(data)
    await state.set_state(MenuState.menu)
    await menu_handler(message, state)

