

from aiogram.fsm.state import StatesGroup, State




class Student_Info(StatesGroup):
    full_name=State()
    birth_date=State()
    class_number=State()
    region_id=State()
    state_id=State()
    school_id=State()
    password=State()
    verify_password=State()
    accept=State()
    ask_login=State()
    ask_login_number=State()