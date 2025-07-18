from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from user.models.user import User
from user.models.student import Student
from university.models.application import StudentApplication
from tift_bot.dispatcher import dp
from aiogram.types import FSInputFile

@dp.message(lambda message: message.text in ("Profile 👤", "Профиль 👤"))
async def profile(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang')
    tg_id = message.from_user.id
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    user = User.objects.filter(tg_id=tg_id).first()
    student = Student.objects.filter(user_id=user.id).first()
    if not student:
        if lang == 'uz':
            await message.answer("⛔ Siz hali hujjat topshirmagansiz.")
        elif lang == 'ru':
            await message.answer("⛔ Вы ещё не подали заявление.")
        return

    student_application = StudentApplication.objects.filter(student_id=student.id).first()
    if not student_application:
        if lang == 'uz':
            await message.answer("⛔ Siz hali hujjat topshirmagansiz.")
        elif lang == 'ru':
            await message.answer("⛔ Вы ещё не подали заявление.")
        return
    if student.qualification == 1:
        qualification = "Middle School"
    elif student.qualification == 2:
        qualification = "College"
    elif student.qualification == 3:
        qualification = "Lyceum"
    elif student.qualification == 4:
        qualification = "University"
    elif student.qualification == 5:
        qualification = "Technical School"
    else:
        qualification = "nomalum"
    ender_icon = "🤵‍♂️" if student.gender == "1" else "🤵‍♀️"
    gender_text = "Erkak" if student.gender == "1" else "Ayol"
    gender_text_ru = "Мужчина" if student.gender == "1" else "Женщина"

    try:
        path="media/"+str(student.photo)
        photo_file = FSInputFile(path)
        send_func = message.answer_photo
    except Exception as e:
        print(e)
        photo_file = None
        send_func = message.answer

    text_uz = (
        f"👤 Shaxsiy ma'lumotlari:\n\n"
        f"📱 Telefon raqam: {user.phone_number}\n"
        f"🪪 Passport: {student.passport_number}\n"
        f"📛 F.I.Sh.: {student.first_name} {student.last_name} {student.father_name}\n"
        f"📟 JSHSHIR: {student.pinfl}\n"
        f"⏱️ Tug'ilgan sana: {student.birth_date}\n"
        f"{ender_icon} Jinsi: {gender_text}\n"
        f"📍 Fuqarolik: {student.citizenship}\n"
        f"🎓 Taʼlim darajasi: {student.name_qualification}\n"
        f"🏫 O‘qigan muassasa: {qualification}\n"
        f"📚 Taʼlim turi: {student_application.program}\n"
        f"🏫 Shakli: {student_application.study_type}\n"
        f"🏛 Fakultet: {student_application.faculty}\n"
        f"📝 Imtihon: {'Online' if student_application.is_online_exam else 'Offline'}\n"
    )

    text_ru = (
        f"👤 Личная информация:\n\n"
        f"📱 Номер телефона: {user.phone_number}\n"
        f"🪪 Паспорт: {student.passport_number}\n"
        f"📛 ФИО: {student.first_name} {student.last_name} {student.father_name}\n"
        f"📟 ПИНФЛ: {student.pinfl}\n"
        f"⏱️ Дата рождения: {student.birth_date}\n"
        f"{ender_icon} Пол: {gender_text_ru}\n"
        f"📍 Гражданство: {student.citizenship}\n"
        f"🎓 Образование: {student.name_qualification}\n"
        f"🏫 Учебное заведение: {qualification}\n"
        f"📚 Тип программы: {student_application.program}\n"
        f"🏫 Форма: {student_application.study_type}\n"
        f"🏛 Факультет: {student_application.faculty}\n"
        f"📝 Экзамен: {'Онлайн' if student_application.is_online_exam else 'Оффлайн'}\n"
    )

    text = text_uz if lang == 'uz' else text_ru

    if photo_file:
        await send_func(photo=photo_file, caption=text)
    else:
        await send_func(text=text)