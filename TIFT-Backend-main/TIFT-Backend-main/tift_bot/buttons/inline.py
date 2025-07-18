from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tift_bot.buttons.text import *


def accept_buttons(language: str = "uz"):
    texts = {
        "uz": ("✅ Ma'lumotlarni tasdiqlash", "🗑 Ma'lumotlarni bekor qilish"),
        "ru": ("✅ Проверка данных", "🗑 Отмена данных")
    }

    accept_text, cancel_text = texts.get(language, texts["uz"])
    accept = InlineKeyboardButton(text=accept_text, callback_data="accepted")
    cancel = InlineKeyboardButton(text=cancel_text, callback_data="cancelled")
    return InlineKeyboardMarkup(inline_keyboard=[[accept], [cancel]])


def back_inline(lang='uz'):
    texts = {
        'uz': ortga,
        'ru': nazad,

    }

    back_text = texts.get(lang, texts['uz'])
    back_button = InlineKeyboardButton(text=back_text, callback_data='back')
    return InlineKeyboardMarkup(inline_keyboard=[[back_button]])


def answer_admin(user_id):
    keyboard1 = InlineKeyboardButton(text="Javob berish 📝", callback_data=f'answer_{user_id}')
    return InlineKeyboardMarkup(inline_keyboard=[[keyboard1]])

def begin_exam(lang='uz'):
    if lang == 'uz':
        text1="✍️ Imtihonni boshlash"
    else:
        text1="✍️ Начать экзамен"
    keyboard1 = InlineKeyboardButton(text=text1, callback_data=f'begin_exam')
    return InlineKeyboardMarkup(inline_keyboard=[[keyboard1]])

def exam_questions(data):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"A) {data['version_a']}", callback_data=f"question_{data['id']}_a"),
         InlineKeyboardButton(text=f"B) {data['version_b']}", callback_data=f"question_{data['id']}_b")],
        [InlineKeyboardButton(text=f"C) {data['version_c']}", callback_data=f"question_{data['id']}_c"),
         InlineKeyboardButton(text=f"D) {data['version_d']}", callback_data=f"question_{data['id']}_d")],
    ])
    return keyboard