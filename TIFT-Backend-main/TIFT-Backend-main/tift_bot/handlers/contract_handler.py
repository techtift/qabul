import tempfile
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from tift_bot.state.MenuState import MenuState
from university.services.generate_contract.generate_contract import generate_student_contract
from user.models.student import Student
from user.models.user import User
from tift_bot.dispatcher import dp

@dp.message(lambda message: message.text in ("📥 Скачать договор", "📥 Shartnomani yuklab olish"))
async def profile(message: Message, state: FSMContext) -> None:
    from tift_bot.handlers.start_handler import menu_handler
    data = await state.get_data()
    lang = data.get('lang', 'uz')
    tg_id = message.from_user.id
    data['tg_id'] = tg_id

    user = User.objects.filter(tg_id=tg_id).first()
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi.")
        return

    student = Student.objects.filter(user_id=user.id).first()
    if not student:
        await message.answer("❌ Talaba ma'lumotlari topilmadi.")
        return

    try:
        response = generate_student_contract(student.id)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        pdf_file = FSInputFile(temp_pdf_path, filename="contract.pdf")
        await message.answer_document(document=pdf_file)

    except Exception as e:
        await message.answer("❌ Shartnoma yaratishda xatolik yuz berdi.")
        return

    await state.set_state(MenuState.menu)
    await menu_handler(message, state)
