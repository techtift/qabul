import re
from aiogram import Bot
from datetime import datetime, date
from aiogram.types import BotCommand
from django.contrib.auth.hashers import make_password
from user.models.user import User
from user.models.sms import OTP
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes


# Formatting number which checks is that uzb number or not
def format_phone_number(phone_number: str):
    phone_number = ''.join(c for c in phone_number if c.isdigit())

    # Prepend +998 if missing
    if phone_number.startswith('998'):
        phone_number = '+' + phone_number
    elif not phone_number.startswith('+998'):
        phone_number = '+998' + phone_number

    # Check final phone number length
    if len(phone_number) == 13:
        return phone_number
    else:
        False


# Removes -sinf from 2-sinf and returns int value of class number
def remove_string(class_string: str) -> int:
    return int(class_string.split('-')[0])


# checks for valid fullname which contains only letters and spaces
def is_valid_full_name(full_name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿʻʼ'`\- ]+", full_name))


# Validates number of years of age and birth date. Returns True if valid, False otherwise.
def validate_date_and_age(date_str, min_age=7):
    # Formatni tekshirish
    pattern = r'^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    if not re.match(pattern, date_str):
        return False

    try:
        birth_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age < min_age:
        return False

    return True


# Bot commands setting
async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Start the bot"),
        BotCommand(command="language", description="📋 Choose your language"),
    ]
    await bot.set_my_commands(commands)


def create_user_service_bot(data):
    tg_id = data.get('tg_id')
    phone_number = data.get('phone_number')
    password = data.get('password')

    opt = OTP.objects.filter(phone_number=phone_number).first()
    if not opt:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
    if not opt.is_verified:
        raise CustomApiException(ErrorCodes.NOT_VERIFIED)

    if User.objects.filter(phone_number=phone_number).exists():
        raise CustomApiException(ErrorCodes.ALREADY_EXISTS, message="User with this phone number already exists.")
    user, created = User.objects.update_or_create(tg_id=tg_id, defaults={
        'phone_number': phone_number,
        'password': make_password(password),
        'registered_by_bot': True,
        'is_verified': True,
    })
    return user


# checks for valid passport info
def passport_number_checker(passport_number: str) -> bool:
    return bool(re.fullmatch(r"^[A-Z]{2}\d{7}$", passport_number))

def get_qualification_value(text: str) -> int | None:
    mapping = {
        # O‘zbekcha
        "🏫 O‘rta maktab": 1,
        "🏫 Kollej": 2,
        "🏫 Litsey": 3,
        "🏫 Universitet": 4,
        "🏫 Texnikum": 5,

        # Ruscha
        "🏫 Средняя школа": 1,
        "🏫 Колледж": 2,
        "🏫 Лицей": 3,
        "🏫 Университет": 4,
        "🏫 Техникум": 5,


    }

    return mapping.get(text.strip())


def validate_exact_date_format(date_str):
    # Formatni REGEX bilan tekshirish: faqat yyyy-mm-dd formatiga mos kelishi kerak
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False

    # Sana mavjudligini tekshirish
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False