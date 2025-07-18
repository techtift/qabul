from aiogram.fsm.state import StatesGroup, State




class ApplicationState(StatesGroup):
    programs = State()
    study_type = State()
    faculty=State()
    passport=State()
    birth_day=State()
    birth_day_take=State()
    student_info=State()
    diploma=State()
    language=State()
    course_choose=State()
    transcript=State()
    qualification=State()
    name_qualification=State()
    additional_number=State()