from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from core.utils import ADMINS_ID
from tift_bot.buttons.inline import answer_admin
from tift_bot.buttons.reply import back, end_conversation
from tift_bot.buttons.text import *
from aiogram.types import Message, CallbackQuery
from tift_bot.dispatcher import bot,dp
from tift_bot.state.AdminState import Admin_Info
from tift_bot.state.LoginState import AskInfo
from tift_bot.state.MenuState import MenuState
from user.models.user import User
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

@dp.message(lambda message: message.text in (uz.get("contact_reply"), ru.get("contact_reply"),
                                             ))
async def to_(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang')
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('contact_admin')"),
            reply_markup=back(lang)
        )
    await state.set_state(Admin_Info.contact)
    return




@dp.message(StateFilter(Admin_Info.contact))
async def contact_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler,user_number_ask
    if message.text in (ortga, nazad):
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    data = await state.get_data()
    lang = data.get('lang')
    user = User.objects.filter(tg_id=message.from_user.id).first()
    if not lang:
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in ("✍️ Suhbatni yakunlash","✍️ Завершить беседу"):
        if lang=='uz':
            await message.answer(text="👍🏻 Suhbat yakunlandi")
        else:
            await message.answer(text="👍🏻 Беседа завершена")
        if user.is_verified and user.registered_by_bot:
            await state.set_state(MenuState.menu)
            await menu_handler(message, state)
            return
        await state.set_state(AskInfo.ask_number)
        await user_number_ask(message, state)
        return

    for admin_id in ADMINS_ID:
        try:
            user_info = (
                f"🧑‍💼 Yuboruvchi: {message.from_user.full_name}\n"
                f"⚙️ Username: @{message.from_user.username or 'yo‘q'}"
            )
            reply_markup = answer_admin(message.from_user.id)
            full_caption = f"{user_info}\n\n{message.caption or ''}"

            if message.text:
                text = f"{user_info}\n\n📝 Xabar matni:\n{message.text}"
                await bot.send_message(chat_id=admin_id, text=text, reply_markup=reply_markup)

            elif message.photo:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=message.photo[-1].file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.video:
                await bot.send_video(
                    chat_id=admin_id,
                    video=message.video.file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.audio:
                await bot.send_audio(
                    chat_id=admin_id,
                    audio=message.audio.file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.voice:
                await bot.send_voice(
                    chat_id=admin_id,
                    voice=message.voice.file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.video_note:
                await bot.send_video_note(
                    chat_id=admin_id,
                    video_note=message.video_note.file_id,
                    reply_markup=reply_markup
                )
                await bot.send_message(chat_id=admin_id, text=user_info, reply_markup=reply_markup)

            elif message.animation:
                await bot.send_animation(
                    chat_id=admin_id,
                    animation=message.animation.file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.document:
                await bot.send_document(
                    chat_id=admin_id,
                    document=message.document.file_id,
                    caption=full_caption,
                    reply_markup=reply_markup
                )

            elif message.sticker:
                await bot.send_sticker(
                    chat_id=admin_id,
                    sticker=message.sticker.file_id
                )
                await bot.send_message(chat_id=admin_id, text=user_info, reply_markup=reply_markup)

            elif message.location:
                await bot.send_location(
                    chat_id=admin_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    reply_markup=reply_markup
                )
                await bot.send_message(chat_id=admin_id, text=user_info, reply_markup=reply_markup)

            elif message.contact:
                await bot.send_contact(
                    chat_id=admin_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name or "",
                    reply_markup=reply_markup
                )
                await bot.send_message(chat_id=admin_id, text=user_info, reply_markup=reply_markup)

            elif message.dice:
                await bot.send_dice(
                    chat_id=admin_id,
                    emoji=message.dice.emoji,
                    reply_markup=reply_markup
                )
                await bot.send_message(chat_id=admin_id, text=user_info, reply_markup=reply_markup)

            else:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"{user_info}\n\n❗ Noma'lum xabar turi",
                    reply_markup=reply_markup
                )

        except (TelegramForbiddenError, TelegramBadRequest):
            continue
        except Exception as e:
            print(f"Xatolik admin {admin_id} ga xabar yuborishda: {e}")

    if lang:
        await message.answer(text=eval(f"{lang}.get('contact_success')"),reply_markup=end_conversation(lang))
    await state.set_state(Admin_Info.contact)
    return




@dp.callback_query(F.data.startswith("answer_"))
async def certificate_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.data.split('_')[1]
    await callback_query.message.answer(text=all.get("admin_answer"))
    await state.set_state(Admin_Info.answer)
    await state.update_data(user_id=user_id)
    return




@dp.message(StateFilter(Admin_Info.answer))
async def answer(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    user_id = data.get('user_id')
    text_header = "📝 Admindan javob:"
    try:
        full_caption = f"{text_header}\n\n{message.caption or ''}"

        if message.text:
            text = f"{text_header}\n\n{message.text}"
            await bot.send_message(chat_id=user_id, text=text)

        elif message.photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=full_caption
            )

        elif message.video:
            await bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=full_caption
            )

        elif message.audio:
            await bot.send_audio(
                chat_id=user_id,
                audio=message.audio.file_id,
                caption=full_caption
            )

        elif message.voice:
            await bot.send_voice(
                chat_id=user_id,
                voice=message.voice.file_id,
                caption=full_caption
            )

        elif message.video_note:
            await bot.send_video_note(chat_id=user_id, video_note=message.video_note.file_id)
            await bot.send_message(chat_id=user_id, text=text_header)

        elif message.animation:
            await bot.send_animation(
                chat_id=user_id,
                animation=message.animation.file_id,
                caption=full_caption
            )

        elif message.document:
            await bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=full_caption
            )

        elif message.sticker:
            await bot.send_sticker(chat_id=user_id, sticker=message.sticker.file_id)
            await bot.send_message(chat_id=user_id, text=text_header)

        elif message.location:
            await bot.send_location(
                chat_id=user_id,
                latitude=message.location.latitude,
                longitude=message.location.longitude
            )
            await bot.send_message(chat_id=user_id, text=text_header)

        elif message.contact:
            await bot.send_contact(
                chat_id=user_id,
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name or ""
            )
            await bot.send_message(chat_id=user_id, text=text_header)

        elif message.dice:
            await bot.send_dice(chat_id=user_id, emoji=message.dice.emoji)
            await bot.send_message(chat_id=user_id, text=text_header)

        else:
            await bot.send_message(chat_id=user_id, text=f"{text_header}\n\n❗ Noma'lum xabar turi")

    except Exception as e:
        print(f"Xatolik foydalanuvchiga yuborishda: {e}")

    await message.answer(text="✅ Xabar yuborildi")
    await state.set_state(MenuState.menu)
    await menu_handler(message, state)
    return



