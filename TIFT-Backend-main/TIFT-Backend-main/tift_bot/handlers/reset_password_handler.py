from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from tift_bot.buttons.text import *
from tift_bot.buttons.reply import get_contact_keyboard, back
from tift_bot.dispatcher import dp
from tift_bot.state.ResetPasswordState import Reset_password
from user.models.user import User
from user.services.reset_password import reset_password_service, verify_reset_code_service,reset_password_confirm_service


async def reset_password_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    phone_number = data.get('phone_number')
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    try:
        response=reset_password_service(phone_number)
        if response.is_sent:
            if lang:
                await message.answer(
                    text=eval(f"{lang}.get('enter_sms')"),
                    reply_markup=back(lang)
                )
            await state.set_state(Reset_password.verify_number)
            return
    except Exception as e:
        if lang:
            print(e)
            await message.answer(
                text=eval(f"{lang}.get('reset_password_sent_sms_error')"),
                reply_markup=get_contact_keyboard(lang)
            )
            await reset_password_handler(message, state)
        return

@dp.message(StateFilter(Reset_password.verify_number))
async def user_number_get(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.registration_handler import user_number_ask
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    phone_number = data.get('phone_number')
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        await user_number_ask(message, state)
        return

    try:
        response=verify_reset_code_service(phone_number,message.text)
        if response:
            if lang:
                await message.answer(
                    text=eval(f"{lang}.get('password_text')"),
                    reply_markup=back(lang)
                )
            await message.answer(text="🫣")
            await state.set_state(Reset_password.password)
            return
    except Exception as e:
        if lang:
            print(e)
            await message.answer(
                text=eval(f"{lang}.get('reset_password_sms_error')"),
                reply_markup=get_contact_keyboard(lang)
            )
        await reset_password_handler(message, state)
        return







@dp.message(StateFilter(Reset_password.password))
async def password_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    await message.delete()
    if message.text in (nazad, ortga):
        await reset_password_handler(message, state)
        return
    data['password'] = message.text
    await state.set_data(data)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('confirm_password_text')"),
            reply_markup=back(lang)
        )

    await state.set_state(Reset_password.verify_password)
    return


@dp.message(StateFilter(Reset_password.verify_password))
async def verify_password_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.registration_handler import user_number_ask
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
        await state.set_state(Reset_password.password)
        return

    if not message.text == data.get("password"):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('confirm_error_text')"),
                reply_markup=back(lang)
            )
        await state.set_state(Reset_password.password)
        return
    try:
        response=reset_password_confirm_service(data.get('phone_number'),data.get("password"))
        if response:
            if lang:
                await message.answer(
                    text=eval(f"{lang}.get('reset_password_success')"),
                    reply_markup=ReplyKeyboardRemove()
                )

            await user_number_ask(message, state)
            return
    except Exception as e:
        await reset_password_handler(message, state)
        return


