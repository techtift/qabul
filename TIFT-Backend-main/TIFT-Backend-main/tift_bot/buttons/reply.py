from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tift_bot.buttons.text import *
from university.models.application import StudentApplication
from university.services.applications.get_applications import get_applications
from university.services.programs.get_study_types import get_study_types
from user.models.student import Student


def get_contact_keyboard(language='uz'):
    text = eval(f"{language}.get('phone_number_ask')")

    contact_button = KeyboardButton(text=text, request_contact=True)
    design = [[contact_button]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, input_field_placeholder="+998901234567")


def menu(user_id, lang='uz'):
    texts = {
        'uz': ("Profile 👤", "Hujjat topshirish ✍️", "Imtihondan o'tish 📝", uz.get("contact_reply"), "📥 Shartnomani yuklab olish",'💤 Hisobdan chiqish'),
        'ru': ("Профиль 👤", "Подать документы ✍️", "Пройти экзамен 📝", ru.get("contact_reply"), "📥 Скачать договор",'💤 Выйти из аккаунта'),
    }

    student = Student.objects.filter(user_id=user_id).first()
    student_application = (
        StudentApplication.objects.filter(student_id=student.id).first()
        if student else None
    )

    text1, text2, text3, text4, text5,text6 = texts[lang]
    btn1 = KeyboardButton(text=text1)
    btn2 = KeyboardButton(text=text2)
    btn3 = KeyboardButton(text=text3)
    btn4 = KeyboardButton(text=text4)
    btn5 = KeyboardButton(text=text5)
    btn6 = KeyboardButton(text=text6)

    if student and student.is_passed_exam:
        layout = [[btn1], [btn4, btn5], [btn6]]
    elif student and student.is_attended_exam:
        layout = [[btn1], [btn4, btn6]]
    elif student_application:
        layout = [[btn1], [btn3, btn4],[btn6]]
    else:
        layout = [[btn1], [btn2, btn4],[btn6]]

    return ReplyKeyboardMarkup(keyboard=layout, resize_keyboard=True)

def language_btn():
    keyboard1 = KeyboardButton(text=uz_text)
    keyboard2 = KeyboardButton(text=ru_text)
    design = [[keyboard1, keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


def back(lang='uz'):
    text = {'uz': ortga, 'ru': nazad}[lang]

    keyboard1 = KeyboardButton(text=text)
    design = [[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


def custom_placeholder(custom_input):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[],
        resize_keyboard=True,
        input_field_placeholder=custom_input
    )
    return keyboard


def programs_choose(lang='uz'):
    application=get_applications().first()
    builder = ReplyKeyboardBuilder()
    if lang=='uz':
        for programs in application.programs.all():
            builder.add(KeyboardButton(text=programs.name_uz))
    else:
        for programs in application.programs.all():
            builder.add(KeyboardButton(text=programs.name_ru))
    btn_texts = {
        'uz': ortga,
        'ru': nazad,
    }

    builder.add(KeyboardButton(text=btn_texts.get(lang, ortga)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def study_type_choose(program_id,lang='uz'):
    study_types=get_study_types(program_id)
    builder = ReplyKeyboardBuilder()
    if lang=='uz':
        for study_type in study_types:
            builder.add(KeyboardButton(text=study_type.name_uz))
    else:
        for study_type in study_types:
            builder.add(KeyboardButton(text=study_type.name_ru))
    btn_texts = {
        'uz': ortga,
        'ru': nazad,
    }

    builder.add(KeyboardButton(text=btn_texts.get(lang, ortga)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def faculty_choose(lang='uz'):
    application = get_applications().first()
    builder = ReplyKeyboardBuilder()
    if lang=='uz':
        for faculty in application.faculties.all():
            builder.add(KeyboardButton(text=faculty.name_uz))
    else:
        for faculty in application.faculties.all():
            builder.add(KeyboardButton(text=faculty.name_ru))
    btn_texts = {
        'uz': ortga,
        'ru': nazad,
    }

    builder.add(KeyboardButton(text=btn_texts.get(lang, ortga)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def lang_choose(lang='uz'):

    btn_texts = {
        'uz': ("O'zbek tili","Rus tili",ortga),
        'ru': ("Узбекский язык", "Русский язык", nazad),
    }
    text1,text2,text3=btn_texts[lang]
    keyboard1 = KeyboardButton(text=text1)
    keyboard2 = KeyboardButton(text=text2)
    keyboard3 = KeyboardButton(text=text3)
    design=[[keyboard1,keyboard2],[keyboard3]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

def course_choose(lang='uz'):
    builder = ReplyKeyboardBuilder()
    for i in range(1,5):
        builder.add(KeyboardButton(text=f"{i}"))
    if lang=='uz':
        builder.add(KeyboardButton(text=ortga))
    else:
        builder.add(KeyboardButton(text=nazad))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def qualification_choose(lang='uz'):
    builder = ReplyKeyboardBuilder()
    if lang == 'uz':
        buttons = [
            "🏫 O‘rta maktab",
            "🏫 Kollej",
            "🏫 Litsey",
            "🏫 Universitet",
            "🏫 Texnikum"
        ]
    elif lang == 'ru':
        buttons = [
            "🏫 Средняя школа",
            "🏫 Колледж",
            "🏫 Лицей",
            "🏫 Университет",
            "🏫 Техникум"
        ]

    for  b in buttons:
        builder.add(KeyboardButton(text=b))
    if lang=='uz':
        builder.add(KeyboardButton(text=ortga))
    else:
        builder.add(KeyboardButton(text=nazad))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def skip(lang='uz'):
    if lang == 'uz':
        skip_text = "⏭️ O'tkazib yuborish"
        back_text = ortga
    elif lang == 'ru':
        skip_text = "⏭️ Пропустить"
        back_text = nazad
    keyboard1 = KeyboardButton(text=skip_text)
    keyboard2 = KeyboardButton(text=back_text)
    design=[[keyboard1,keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


def reset_password(lang='uz'):
    if lang == 'uz':
        text1="📟 Parolni o'zgartirish"
        text2=ortga
    else:
        text1="📟 Изменить пароль"
        text2=nazad
    keyboard1 = KeyboardButton(text=text1)
    keyboard2 = KeyboardButton(text=text2)
    design=[[keyboard1,keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


def end_conversation(lang='uz'):
    if lang == 'uz':
        text1="✍️ Suhbatni yakunlash"
    else:
        text1="✍️ Завершить беседу"
    keyboard1 = KeyboardButton(text=text1)
    design=[[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)