from aiogram.fsm.state import StatesGroup, State



class AskInfo(StatesGroup):
    ask_number = State()
    get_number=State()
    verify_number=State()
    ask_login=State()
    password=State()
    verify_password=State()