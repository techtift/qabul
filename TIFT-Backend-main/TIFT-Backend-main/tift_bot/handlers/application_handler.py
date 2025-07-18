from aiogram.filters import StateFilter
import requests, asyncio
from core.exceptions.exception import CustomApiException
from core.utils import TOKEN
from tift_bot.buttons.reply import (programs_choose, study_type_choose, faculty_choose, back, lang_choose,
                                    course_choose, qualification_choose, skip)
from tift_bot.state.AplicationState import ApplicationState
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,  FSInputFile
from django.db.models import Q
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from tift_bot.utils import passport_number_checker, format_phone_number, get_qualification_value, \
    validate_exact_date_format
from university.models.faculty import Faculty
from university.models.program import Program
from university.models.study_type import StudyType
from university.services.applications.create_student_application import create_student_application
from university.services.applications.get_applications import get_applications
from user.models.student import Student
from user.models.user import User
from tift_bot.dispatcher import dp
from tift_bot.buttons.text import *
from tift_bot.state.MenuState import MenuState
from user.services.create_student_by_passport import student_create_by_passport_service
from django.core.files.base import ContentFile
from aiohttp import ClientSession


@dp.message(lambda message: message.text in ("Подать документы ✍️", "Hujjat topshirish ✍️"))
async def profile(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang')
    tg_id = message.from_user.id
    user = User.objects.filter(tg_id=tg_id).first()
    data['user_id'] = user.id
    await state.update_data(data)
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang == "uz":
        await message.answer(
            text=uz.get("overview"),parse_mode='HTML')
        await message.answer(text=uz.get('choose_program'), reply_markup=programs_choose(lang))
    else:
        await message.answer(
            text=ru.get("overview"),parse_mode='HTML')
        await message.answer(text=ru.get('choose_program'), reply_markup=programs_choose(lang))
    await state.set_state(ApplicationState.programs)
    return


@dp.message(StateFilter(ApplicationState.programs))
async def program_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    if message.text in (ortga, nazad):
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    lang = data.get('lang')
    application = get_applications().first()
    data['application_id'] = application.id
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)

    try:
        programs_id = Program.objects.filter(Q(name_uz=message.text) | Q(name_ru=message.text)).first().id
    except AttributeError:
        await message.answer(text="Server side error")
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return

    data['program_id'] = programs_id
    if message.text in ("O'qishni ko'chirib o'tish", "Перевод"):
        if lang == 'uz':
            await message.answer(text=uz.get("choose_course_text"), reply_markup=course_choose(lang))
        else:
            await message.answer(text=ru.get('choose_course_text'), reply_markup=course_choose(lang))
        data['is_transfer'] = True
        await state.update_data(data)
        await state.set_state(ApplicationState.course_choose)
        return

    if lang:
        await message.answer(
            text=eval(f"{lang}.get('choose_study_type')"),
            reply_markup=study_type_choose(programs_id,lang)
        )
    await state.update_data(data)
    await state.set_state(ApplicationState.study_type)
    return


@dp.message(StateFilter(ApplicationState.study_type))
async def study_type_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang')
    tg_id=data.get('tg_id')
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if lang == "uz":
            await message.answer(text=uz.get('choose_program'), reply_markup=programs_choose(lang))
        else:
            await message.answer(text=ru.get('choose_program'), reply_markup=programs_choose(lang))
        await state.set_state(ApplicationState.programs)
        return
    try:
        study_type_id = StudyType.objects.filter(Q(name_uz=message.text) | Q(name_ru=message.text)).first().id
    except AttributeError:
        await message.answer(text="Server side error")
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    data['study_type_id'] = study_type_id
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('choose_faculty')"),
            reply_markup=faculty_choose(lang)
        )
    await state.update_data(data)
    await state.set_state(ApplicationState.faculty)
    return


@dp.message(StateFilter(ApplicationState.faculty))
async def faculty_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang')
    tg_id=data.get('tg_id')
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('choose_study_type')"),
                reply_markup=study_type_choose(data.get('program_id'),lang)
            )
        await state.set_state(ApplicationState.study_type)
        return
    try:
        faculty_id = Faculty.objects.filter(Q(name_uz=message.text) | Q(name_ru=message.text)).first().id
    except AttributeError:
        await message.answer(text="Server side error")
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    data['faculty_id'] = faculty_id
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('enter_passport_info')"),
            reply_markup=back(lang)
        )
    await state.update_data(data)
    await state.set_state(ApplicationState.passport)
    return


@dp.message(StateFilter(ApplicationState.passport))
async def passport_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get('lang')
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if data.get('is_transfer'):
            if lang == 'uz':
                await message.answer(text=uz.get('ask_transcript'), reply_markup=back(lang))
            else:
                await message.answer(text=ru.get('ask_transcript'), reply_markup=back(lang))
            await state.set_state(ApplicationState.transcript)
            return
        else:
            if lang:
                await message.answer(
                    text=eval(f"{lang}.get('choose_faculty')"),
                    reply_markup=faculty_choose(lang)
                )
            await state.set_state(ApplicationState.faculty)
            return
    passport = passport_number_checker(message.text)
    if not passport:
        if lang == 'uz':
            await message.answer(text=uz.get('ask_right_pass'), reply_markup=back(lang))
        else:
            await message.answer(text=uz.get('ask_right_pass'), reply_markup=back(lang))
        return
    students = Student.objects.filter(passport_number=message.text).all()
    if students.exists():
        if lang == 'uz':
            await message.answer(text=uz.get('passport_already_exists'))
        else:
            await message.answer(text=ru.get('passport_already_exists'))
        return
    data['passport'] = message.text
    await state.update_data(data)
    await state.set_state(ApplicationState.birth_day)
    await birth_date_handler(message, state)
    return


@dp.message(StateFilter(ApplicationState.birth_day))
async def birth_date_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        user = User.objects.filter(tg_id=message.from_user.id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('enter_passport_info')"),
                reply_markup=back(lang)
            )
        await state.update_data(data)
        await state.set_state(ApplicationState.passport)
        return
    if lang:
        msg=await message.answer(
            text=eval(f"{lang}.get('birth_info_get')"),
            reply_markup=await DialogCalendar().start_calendar()
        )
        await state.update_data(msg_id=msg.message_id)
    await state.set_state(ApplicationState.birth_day_take)
    return


@dp.callback_query(DialogCalendarCallback.filter())
async def process_simple_calendar(callback_query, callback_data, state: FSMContext):
    from tift_bot.handlers.start_handler import menu_handler
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if not selected:
        return
    data = await state.get_data()
    lang = data.get("lang")
    if not lang:
        lang = "uz"
    if callback_query.message.text in (ortga, nazad):
        if lang:
            await callback_query.message.answer(
                text=eval(f"{lang}.get('enter_passport_info')"),
                reply_markup=back(lang)
            )
        await state.update_data(data)
        await state.set_state(ApplicationState.passport)
        return
    data['birth_date'] = date.strftime('%Y-%m-%d')
    await state.set_data(data)
    if lang == 'uz':
        await callback_query.message.answer(text=uz.get('verify_pending'))
    else:
        await callback_query.message.answer(text=ru.get('verify_pending'))
    student = Student.objects.filter(user_id=data.get('user_id')).first()
    if student:
        await state.set_state(ApplicationState.student_info)
        await student_info_handler(callback_query.message, state)
        return
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            student_create_by_passport_service,
            data['birth_date'],
            data['passport'],
            data['user_id']
        )
        print(response.pinfl)
    except (CustomApiException, requests.exceptions.RequestException, Exception) as e:
        if lang == 'uz':
            await callback_query.message.answer(text=uz.get('not_verified'))
        else:
            await callback_query.message.answer(
                    text=ru.get('not_verified'),
                    reply_markup=back(lang)
                )
        await state.set_state(MenuState.menu)
        await menu_handler(callback_query.message, state)
        return
    await state.set_state(ApplicationState.student_info)
    await student_info_handler(callback_query.message, state)


@dp.message(StateFilter(ApplicationState.birth_day_take))
async def birthday_take_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data['msg_id']:
        await message.bot.delete_message(message.chat.id, message_id=data['msg_id'])
        del data['msg_id']
        await state.update_data(data)
    lang = data.get("lang")
    if not lang:
        lang = "uz"
    if message.text in (ortga, nazad):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('enter_passport_info')"),
                reply_markup=back(lang)
            )
        await state.update_data(data)
        await state.set_state(ApplicationState.passport)
        return
    if not validate_exact_date_format(message.text):
        if lang=='uz':
            await message.answer(text=uz.get('wrong_birth'))
        else:
            await message.answer(text=ru.get('wrong_birth'))
        return
    data['birth_date'] = message.text
    await state.set_data(data)
    if lang == 'uz':
        await message.answer(text=uz.get('verify_pending'))
    else:
        await message.answer(text=ru.get('verify_pending'))
    student = Student.objects.filter(user_id=data.get('user_id')).first()
    if student:
        await state.set_state(ApplicationState.student_info)
        await student_info_handler(message, state)
        return
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            student_create_by_passport_service,
            data['birth_date'],
            data['passport'],
            data['user_id']
        )
        print(response.pinfl)
    except (CustomApiException, requests.exceptions.RequestException, Exception) as e:
        if lang == 'uz':
            await message.answer(text=uz.get('not_verified'))
        else:
            await message.answer(
                text=ru.get('not_verified'),
                reply_markup=back(lang)
            )
        from tift_bot.handlers.start_handler import menu_handler
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    await state.set_state(ApplicationState.student_info)
    await student_info_handler(message, state)


@dp.message(StateFilter(ApplicationState.student_info))
async def student_info_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    tg_id = data.get('tg_id')
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if lang:
            await message.answer(
                text=eval(f"{lang}.get('enter_passport_info')"),
                reply_markup=back(lang)
            )
        await state.update_data(data)
        await state.set_state(ApplicationState.passport)
        return
    student = Student.objects.filter(user_id=data.get('user_id')).first()

    text_uz = (
        f"👤 <b>Shaxsiy ma'lumotlaringiz</b>:\n\n"
        f"📛 <b>Ismi:</b> {student.first_name}\n"
        f"👨‍👩‍👧 <b>Familiyasi:</b> {student.last_name}\n"
        f"🧔 <b>Otasining ismi:</b> {student.father_name}\n"
        f"🎂 <b>Tug‘ilgan sana:</b> {student.birth_date}\n"
        f"🌍 <b>Fuqaroligi:</b> {student.citizenship}\n"
        f"📍 <b>Tug‘ilgan joyi:</b> {student.birth_place}\n"
        f"🆔 <b>PINFL:</b> {student.pinfl}\n"
        f"🛂 <b>Pasport seriyasi va raqami:</b> {student.passport_number}\n"
        f"🎓 <b>Ta’lim darajasi:</b> {student.qualification}\n"
        f"🏫 <b>O‘qigan muassasa:</b> {student.name_qualification}\n\n"

    )

    text_ru = (
        f"👤 <b>Личные данные</b>:\n\n"
        f"📛 <b>Имя:</b> {student.first_name}\n"
        f"👨‍👩‍👧 <b>Фамилия:</b> {student.last_name}\n"
        f"🧔 <b>Отчество:</b> {student.father_name} {'СЫН' if student.gender == '1' else 'ДОЧЬ'}\n\n"
        f"🎂 <b>Дата рождения:</b> {student.birth_date}\n"
        f"🌍 <b>Гражданство:</b> {student.citizenship}\n"
        f"📍 <b>Место рождения:</b> {student.birth_place}\n"
        f"🆔 <b>ПИНФЛ:</b> {student.pinfl}\n"
        f"🛂 <b>Серия и номер паспорта:</b> {student.passport_number}\n"
        f"🎓 <b>Уровень образования:</b> {student.qualification}\n"
        f"🏫 <b>Наименование учебного заведения:</b> {student.name_qualification}\n\n"

    )
    if lang == 'uz':
        text = text_uz
    else:
        text = text_ru
    try:
        if student.photo:
            path = "media/" + str(student.photo)
            photo_file = FSInputFile(path)
            await message.answer_photo(photo=photo_file, caption=text, reply_markup=back(lang), parse_mode='HTML')
    except:
        await message.answer(text=text, reply_markup=back(lang), parse_mode='HTML')
    if student.qualification and student.name_qualification:
        if not student.diploma:
            await state.set_state(ApplicationState.diploma)
            if lang == 'uz':
                await message.answer(
                    text=uz.get('ask_diploma'),
                    reply_markup=back(lang)
                )
            else:
                await message.answer(
                    text=ru.get('ask_diploma'),
                    reply_markup=back(lang)
                )
            return
        await state.set_state(ApplicationState.additional_number)
        if lang == 'uz':
            await message.answer(text=uz.get('additional_ask'), reply_markup=lang_choose(lang))
        else:
            await message.answer(text=ru.get('additional_ask'), reply_markup=lang_choose(lang))
        return

    await state.set_state(ApplicationState.qualification)
    if lang == 'uz':
        await message.answer(text=uz.get('ask_qualification'), reply_markup=qualification_choose(lang))
    else:
        await message.answer(text=ru.get('ask_qualification'), reply_markup=qualification_choose(lang))
    return


@dp.message(StateFilter(ApplicationState.qualification))
async def qualification_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    if message.text in (ortga, nazad):
        await state.set_state(ApplicationState.student_info)
        await student_info_handler(message, state)
    qualification = get_qualification_value(message.text)
    if isinstance(qualification, int):
        student = Student.objects.filter(user_id=data.get('user_id')).first()
        student.qualification = qualification
        student.save()
    else:
        if lang == 'uz':
            await message.answer(text=uz.get('use_btn'))
        else:
            await message.answer(text=ru.get('use_btn'))
        return
    if lang == 'uz':
        await message.answer(text=uz.get('name_qualification_ask'), reply_markup=back(lang))
    else:
        await message.answer(text=ru.get('name_qualification_ask'))
    await state.set_state(ApplicationState.name_qualification)
    return


@dp.message(StateFilter(ApplicationState.name_qualification))
async def name_qualification_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    tg_id = data.get('tg_id')
    user_id = data.get('user_id')
    data['qual_ask']=True
    await state.update_data(data)
    if message.text in (ortga, nazad):
        if lang == 'uz':
            await message.answer(text=uz.get('ask_qualification'), reply_markup=qualification_choose(lang))
        else:
            await message.answer(text=ru.get('ask_qualification'), reply_markup=qualification_choose(lang))
        await state.set_state(ApplicationState.qualification)
        return
    student = Student.objects.filter(user_id=user_id).first()
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    student.name_qualification = message.text
    student.save()

    if not student.diploma:
        await state.set_state(ApplicationState.diploma)
        if lang == 'uz':
            await message.answer(
                text=uz.get('ask_diploma'),
                reply_markup=back(lang)
            )
        else:
            await message.answer(
                text=ru.get('ask_diploma'),
                reply_markup=back(lang)
            )
        return


@dp.message(StateFilter(ApplicationState.diploma))
async def diploma_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    tg_id = data.get('tg_id')
    user_id = data.get('user_id')
    data['diploma_ask']=True
    await state.update_data(data)
    if message.text in (ortga, nazad) and data.get('qual_ask'):
        if lang == 'uz':
            await message.answer(text=uz.get('name_qualification_ask'), reply_markup=back(lang))
        else:
            await message.answer(text=ru.get('name_qualification_ask'))
        await state.set_state(ApplicationState.name_qualification)
        return
    elif message.text in (ortga, nazad) :
        await state.set_state(ApplicationState.student_info)
        await student_info_handler(message, state)
        return
    student = Student.objects.filter(user_id=user_id).first()
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.document:
        document = message.document.file_id
        file_name = message.document.file_name
        file_info = await message.bot.get_file(document)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        async with ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status == 200:
                    file_data = await resp.read()

                    student.diploma.save(file_name, ContentFile(file_data))
                    student.save()
                    if lang == 'uz':
                        await message.answer(text=uz.get('file_upload_succes'))
                    else:
                        await message.answer(text=ru.get('file_upload_succes'))
                else:
                    if lang == 'uz':
                        await message.answer(text=uz.get('file_upload_no'))
                    else:
                        await message.answer(text=ru.get('file_upload_no'))


    if lang == 'uz':
        await message.answer(text=uz.get('additional_ask'), reply_markup=skip(lang))
    else:
        await message.answer(text=ru.get('additional_ask'), reply_markup=skip(lang))
    await state.set_state(ApplicationState.additional_number)
    return

@dp.message(StateFilter(ApplicationState.additional_number))
async def additional_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    if message.text in (ortga, nazad) and data.get('diploma_ask'):
        await state.set_state(ApplicationState.diploma)
        if lang == 'uz':
            await message.answer(
                text=uz.get('ask_diploma'),
                reply_markup=back(lang)
            )
        else:
            await message.answer(
                text=ru.get('ask_diploma'),
                reply_markup=back(lang)
            )
        return
    elif message.text in (ortga, nazad):
        await state.set_state(ApplicationState.student_info)
        await student_info_handler(message, state)
        return

    if message.text in ("⏭️ O'tkazib yuborish", "⏭️ Пропустить"):
        if lang == 'uz':
            await message.answer(text=uz.get('language_choose'), reply_markup=lang_choose(lang))
        else:
            await message.answer(text=ru.get('language_choose'), reply_markup=lang_choose(lang))
        await state.set_state(ApplicationState.language)
        return
    if format_phone_number(message.text):
        student = Student.objects.filter(user_id=data.get('user_id')).first()
        student.additional_number = format_phone_number(message.text)
        student.save()
    if lang == 'uz':
        await message.answer(text=uz.get('language_choose'), reply_markup=lang_choose(lang))
    else:
        await message.answer(text=ru.get('language_choose'), reply_markup=lang_choose(lang))
    await state.set_state(ApplicationState.language)
    return

@dp.message(StateFilter(ApplicationState.language))
async def language_handler(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang')
    tg_id=data.get('tg_id')
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if lang == 'uz':
            await message.answer(text=uz.get('additional_ask'), reply_markup=skip(lang))
        else:
            await message.answer(text=ru.get('additional_ask'), reply_markup=skip(lang))
        await state.set_state(ApplicationState.additional_number)
        return

    if message.text in ("O'zbek tili", "Узбекский язык"):
        data['lang'] = 'uz'
    else:
        data['lang'] = 'ru'
    try:
        create_student_application(data, data['user_id'])
    except Exception as e:
        print(e)
        await message.answer(text="Server side error")
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    else:
        if lang == 'uz':
            await message.answer(text=uz.get('info_upload_succes'))
        else:
            await message.answer(text=ru.get('info_upload_succes'))

    await state.set_state(MenuState.menu)
    await menu_handler(message, state)
    return


@dp.message(StateFilter(ApplicationState.course_choose))
async def course_choose_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    tg_id = data.get('tg_id')

    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if message.text in (ortga, nazad):
        if message.text in (ortga, nazad):
            if lang == "uz":
                await message.answer(text=uz.get('choose_program'), reply_markup=programs_choose(lang))
            else:
                await message.answer(text=ru.get('choose_program'), reply_markup=programs_choose(lang))
            await state.set_state(ApplicationState.programs)
            return
    if message.text.isdigit():
        data['transfer_level'] = int(message.text)
        await state.update_data(data)
    else:
        if lang == 'uz':
            await message.answer(text=uz.get('use_btn'))
        else:
            await message.answer(text=ru.get('use_btn'))
        return
    if lang == 'uz':
        await message.answer(text=uz.get('ask_transcript'), reply_markup=back(lang))
    else:
        await message.answer(text=ru.get('ask_transcript'), reply_markup=back(lang))
    await state.set_state(ApplicationState.transcript)
    return


@dp.message(StateFilter(ApplicationState.transcript))
async def transcript_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang")
    tg_id = data.get('tg_id')
    if message.text in (ortga, nazad):
        if lang == 'uz':
            await message.answer(text=uz.get('choose_course_text'), reply_markup=course_choose(lang))
        else:
            await message.answer(text=ru.get('choose_course_text'), reply_markup=course_choose(lang))
        data['is_transfer'] = True
        await state.update_data(data)
        await state.set_state(ApplicationState.course_choose)
        return
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    if not message.document:
        if lang == 'uz':
            await message.answer("📄 Iltimos, transcript faylini yuboring.")
        else:
            await message.answer("📄 Пожалуйста, отправьте файл с транскриптом.")
        return
    if message.document:
        document = message.document.file_id
        file_name = message.document.file_name
        file_info = await message.bot.get_file(document)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        async with ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status == 200:
                    file_data = await resp.read()
                    data['transcript'] = ContentFile(file_data, name=file_name)
                    print(data)
        await state.update_data(data=data)
    if lang:
        await message.answer(
            text=eval(f"{lang}.get('enter_passport_info')"),
            reply_markup=back(lang)
        )
    await state.update_data(data)
    await state.set_state(ApplicationState.passport)
    return
