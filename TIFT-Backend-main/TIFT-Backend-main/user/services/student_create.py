from user.models.student import Student
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes


def student_create_service(user_id, data):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise CustomApiException(
            ErrorCodes.NOT_FOUND,
            "User with the given ID does not exist."
        )

    # Remove "is_verified" from here, that's only for User model
    student_fields = {
        "user": user,
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "father_name": data.get('father_name'),
        "additional_phone_number": data.get('additional_phone_number'),
        "birth_date": data.get('birth_date'),
        "birth_place": data.get('birth_place'),
        "citizenship": data.get('citizenship'),
        "passport_number": data.get('passport_number'),
        "qualification": data.get('qualification'),
        "name_qualification": data.get('name_qualification'),
    }
    if data.get('diploma'):
        student_fields['diploma'] = data.get('diploma')
    if data.get('photo'):
        student_fields['photo'] = data.get('photo')

    student = Student.objects.create(**student_fields)
    return student