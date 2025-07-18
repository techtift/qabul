from user.models.sms import OTP, UserSMS
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from datetime import datetime, timedelta
import secrets
from core.utils import send_sms_message
from django.utils import timezone


def reset_password_service(phone_number):
    if not User.objects.filter(phone_number=phone_number, is_verified=True).exists():
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Bu telefon raqami bilan foydalanuvchi mavjud emas.")

    code = str(secrets.randbelow(900000) + 100000)  # Secure 6-digit code
    expires_at = timezone.now() + timedelta(minutes=5)

    OTP.objects.filter(phone_number=phone_number).delete()
    otp = OTP.objects.create(phone_number=phone_number, code=code, expires_at=expires_at)

    message = f"Sizning saytga kirish uchun tasdiqlash kodingiz:\n@qabul.tift.uz #{code}"
    sms = UserSMS.objects.create(text=message, category='password')

    response = send_sms_message(phone_number, message)
    if response.status_code != 200:
        raise CustomApiException(ErrorCodes.SMS_NOT_SENT, "SMS yuborishda xatolik yuz berdi.")

    sms.is_sent = True
    sms.save()
    return sms

def verify_reset_code_service(phone_number, code):
    otp = OTP.objects.filter(phone_number=phone_number, code=code).first()
    if not otp:
        raise CustomApiException(ErrorCodes.INVALID_INPUT, "Kiritilgan kod noto'g'ri yoki mavjud emas.")
    if otp.expires_at < timezone.now():
        otp.delete()
        raise CustomApiException(ErrorCodes.EXPIRED_OTP, "Kiritilgan kodning muddati tugagan.")
    otp.delete()
    return True

def reset_password_confirm_service(phone_number, new_password):
    user = User.objects.filter(phone_number=phone_number, is_verified=True).first()
    if not user:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Bu telefon raqami bilan foydalanuvchi mavjud emas.")
    user.set_password(new_password)
    user.save()
    return True

