import tempfile
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from tift_bot.buttons.inline import begin_exam, exam_questions
from tift_bot.buttons.reply import menu, back
from tift_bot.state.MenuState import MenuState
from university.models.application import StudentApplication
from university.services.generate_contract.generate_contract import generate_student_contract
from university.services.questions.check_questions import check_questions
from university.services.questions.get_questions_by_faculty import get_questions_by_faculty
from user.models.student import Student
from user.models.user import User
from tift_bot.dispatcher import dp
from tift_bot.buttons.text import *

@dp.message(lambda message: message.text in ("Пройти экзамен 📝","Imtihondan o'tish 📝"))
async def profile(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang')
    tg_id = message.from_user.id
    data['tg_id'] = tg_id
    user = User.objects.filter(tg_id=tg_id).first()
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi.")
        return

    student = Student.objects.filter(user_id=user.id).first()
    student_application = StudentApplication.objects.filter(student_id=student.id).first() if student else None
    if student.is_attended_exam:
        if lang=='uz':
            await message.answer(text="📝 Siz imtihonda faqatgina bir marta qatnasha olasiz")
        else:
            await message.answer(text="📝 Вы можете участвовать в экзамене только один раз")
        await state.set_state(MenuState.menu)
        await menu_handler(message,state)
        return
    if not student or not student_application:
        lang = user.lang if user and user.lang else 'uz'
        await state.update_data(lang=lang)

        if lang == 'uz':
            await message.answer("⛔ Siz hali ariza topshirmagansiz.", reply_markup=menu(lang))
        else:
            await message.answer("⛔ Вы ещё не подали заявление.", reply_markup=menu(lang))
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    data['user_id'] = user.id
    await state.update_data(data)
    if not lang:
        user = User.objects.filter(tg_id=tg_id).first()
        lang = user.lang if user else 'uz'
        await state.update_data(lang=lang)
    response=get_questions_by_faculty(user_id=user.id)
    if response==[]:
        if lang == 'uz':
            await message.answer(text="😞 Siz uchun hech qanday imtihonlar topilmadi")
        else:
            await message.answer(text="😞 Для вас не найдено ни одного экзамена")
        await state.set_state(MenuState.menu)
        await menu_handler(message, state)
        return
    path = "tift_bot/media/20.png"
    photo_file = FSInputFile(path)
    await message.answer_photo(photo=photo_file,reply_markup=back(lang))
    if lang == 'uz':
        await message.answer(text=f"Sizda {response[0].get('subject_name')} va {response[1].get('subject_name')} fanlaridan imtihon savollari bor." ,reply_markup=begin_exam(lang))
    else:
        await message.answer(
            text=f"У вас есть экзаменационные вопросы по предметам {response[0].get('subject_name')} и {response[1].get('subject_name')}.",
            reply_markup=begin_exam(lang)
        )

@dp.callback_query(F.data.startswith("begin_exam"))
async def begin_exam_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.delete()

    data = await state.get_data()
    tg_id = data.get('tg_id')
    lang = data.get('lang', 'uz')

    user = User.objects.filter(tg_id=tg_id).first()
    student = Student.objects.filter(user_id=user.id).first()
    student.is_attended_exam = True
    student.save()
    response = get_questions_by_faculty(user_id=user.id)

    if not response or not response[0]['questions']:
        if lang == 'uz':
            await callback_query.message.answer(text=uz.get('no_questions'))
        else:
            await callback_query.message.answer(text=ru.get('no_questions'))
        return

    await state.update_data(
        questions_1=response[0]['questions'],
        questions_2=response[1]['questions'],
        question_index=0,
        subject_index=1
    )

    first_question = response[0]['questions'][0]
    await callback_query.message.answer(
        text=f"1. {first_question.get('question_text')}",
        reply_markup=exam_questions(first_question)
    )


@dp.callback_query(F.data.startswith("question_"))
async def answer_exam_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    data = await state.get_data()

    subject_index = data.get("subject_index", 1)
    question_index = data.get("question_index", 0) + 1

    callback_data = callback_query.data
    _, qid, selected = callback_data.split("_")

    answers = data.get("answers", [])
    answers.append({
        "question_id": int(qid),
        "selected": selected
    })

    await state.update_data(answers=answers)

    if subject_index == 1:
        questions = data.get("questions_1", [])
    else:
        questions = data.get("questions_2", [])

    if question_index >= len(questions):

        if subject_index == 1 and data.get("questions_2"):
            await state.update_data(
                subject_index=2,
                question_index=0
            )
            next_question = data["questions_2"][0]
            await callback_query.message.edit_text(
                text=f"1. {next_question.get('question_text')}",
                reply_markup=exam_questions(next_question)
            )
            return
        else:
            tg_id = data.get("tg_id")
            user = User.objects.filter(tg_id=tg_id).first()
            response={}
            await callback_query.message.delete()
            try:
                response=check_questions(user_id=user.id, data=data.get("answers"))
            except Exception as e:
                response['passed']=False
            from tift_bot.handlers.start_handler import menu_handler
            lang = data.get("lang")
            if response.get('passed'):
                if lang=="uz":
                    await callback_query.message.answer(text=uz.get('succes_exam'))
                else:
                    await callback_query.message.answer(text=ru.get("succes_exam"))
                student=Student.objects.filter(user_id=user.id).first()
                response = generate_student_contract(student.id)

                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                    temp_pdf.write(response.content)
                    temp_pdf_path = temp_pdf.name

                pdf_file = FSInputFile(temp_pdf_path, filename="contract.pdf")
                await callback_query.message.answer_document(document=pdf_file)

            else:
                if lang=="uz":
                    await callback_query.message.answer(text=uz.get('no_succes_exam'))
                else:
                    await callback_query.message.answer(text=ru.get("no_succes_exam"))
            await state.set_state(MenuState.menu)
            await menu_handler(callback_query.message, state)
            return



    current_question = questions[question_index]
    await callback_query.message.edit_text(
        text=f"{question_index+1}. {current_question.get('question_text')}",
        reply_markup=exam_questions(current_question)
    )

    await state.update_data(question_index=question_index)
