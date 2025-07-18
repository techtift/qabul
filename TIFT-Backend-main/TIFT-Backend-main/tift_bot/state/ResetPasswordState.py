from aiogram.fsm.state import StatesGroup, State




class Reset_password(StatesGroup):
    verify_number=State()
    verify_password=State()
    password=State()
    ask_number=State()
    get_number=State()