from user.models.sms import OTP, UserSMS
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from datetime import datetime, timedelta
import secrets
from core.utils import send_sms_message
from django.utils import timezone


def create_otp_service(phone_number):
    """
    Telefon raqam uchun OTP kod yaratish va saqlash.
    """
    if User.objects.filter(phone_number=phone_number, is_verified=True).exists():
        raise CustomApiException(
            ErrorCodes.ALREADY_EXISTS,
            "Bu telefon raqami bilan foydalanuvchi mavjud.",
        )

    code = str(secrets.randbelow(900000) + 100000)  # Secure 6-digit code
    expires_at = datetime.now() + timedelta(minutes=5)  # 5 daqiqadan keyin eskiradi

    # Eski OTP larni o'chirish
    OTP.objects.filter(phone_number=phone_number).delete()

    # Yangi OTP yaratish
    otp = OTP.objects.create(
        phone_number=phone_number,
        code=code,
        expires_at=expires_at
    )

    otp.save()
    # SMS yuborish
    message = f"Sizning saytga kirish uchun tasdiqlash kodingiz:\n@qabul.tift.uz #{code}"
    sms = UserSMS.objects.create(
        text=message,
        category='password'
    )
    sms.save()
    
    # SMS yuborish funksiyasi
    response = send_sms_message(phone_number, message)

    if response.status_code != 200:
        raise CustomApiException(
            ErrorCodes.SMS_NOT_SENT,
            "SMS yuborishda xatolik yuz berdi.",
        )
    # SMS statusini yangilash
    sms.is_sent = True
    sms.save()

    return sms


def verify_otp(phone_number, input_code):
    otp = OTP.objects.filter(phone_number=phone_number).first()
    if not otp:
        raise CustomApiException(
            ErrorCodes.NOT_FOUND,
            "OTP topilmadi.",
        )
    
    if otp.expires_at < timezone.now(): 
        raise CustomApiException(
            ErrorCodes.EXPIRED_OTP,
            "OTP muddati o'tgan.",
        )
    
    if otp.code != input_code:
        raise CustomApiException(
            ErrorCodes.INVALID_INPUT,
            "Kiritilgan kod noto'g'ri.",
        )
    
    otp.is_verified = True
    otp.save()
    return True
