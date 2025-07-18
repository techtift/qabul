from core.exceptions.error_messages import ErrorCodes
from core.exceptions.exception import CustomApiException
from user.models.user import User
from user.models.student import Student

def update_student_info_service(user_id, data):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "User with the given ID does not exist.")

    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Student with the given user ID does not exist.")

    # Validate additional_phone_number
    additional_phone_number = data.get('additional_phone_number', student.additional_phone_number)
    if additional_phone_number and len(additional_phone_number) > 15:
        raise CustomApiException(
            ErrorCodes.VALIDATION_FAILED,
            "Additional phone number must not be longer than 15 characters."
        )

    student.diploma = data.get('diploma', student.diploma)
    student.qualification = data.get('qualification', student.qualification)
    student.name_qualification = data.get('name_qualification', student.name_qualification)
    student.additional_phone_number = additional_phone_number
    student.is_registred = True
    student.save()

    return student
