import requests
from user.models.student import Student
from user.models.user import User
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
import base64
from django.core.files.base import ContentFile
from core.utils import MyGovClient

my_gov_client = MyGovClient()

def student_create_by_passport_service(birth_date, passport_number, user_id):
    # Validate existing student
    if Student.objects.filter(passport_number=passport_number).exists():
        raise CustomApiException(ErrorCodes.ALREADY_EXISTS, "Student with this PINFL or passport number already exists.")

    # Validate user
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "User with the given ID does not exist.")

    # API calls
    try:
        get_student_document_info = my_gov_client.get_document_info(
            birth_date=birth_date,
            passport_number=passport_number
        )
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 408:
            raise CustomApiException(
                ErrorCodes.TIMEOUT,
                "MyGov API did not respond in time. Please try again later."
            )
        else:
            raise CustomApiException(
                ErrorCodes.TIMEOUT,
                f"MyGov API error: {str(e)}"
            )
    print(f"\nget_student_document_info: {get_student_document_info}\n")
    if not get_student_document_info.get("data", []):
        raise CustomApiException(ErrorCodes.NOT_FOUND, "No student document info found for the provided details.")
    pinfl = get_student_document_info.get("data", {})[0].get("current_pinpp")
    get_lyceum_graduate = my_gov_client.get_lyceum_graduate(pinfl=pinfl)
    get_diploma_info = my_gov_client.get_diploma_info(pinfl=pinfl)
    get_e_shahodatnoma_info = my_gov_client.get_e_shahodatnoma_info(pinfl=pinfl)
    get_student_address = my_gov_client.get_student_address(pinfl=pinfl)

    # Log responses
    print(f"\nget_lyceum_graduate: {get_lyceum_graduate}\n")
    print(f"\nget_diploma_info: {get_diploma_info}\n")
    print(f"\nget_e_shahodatnoma_info: {get_e_shahodatnoma_info}\n")
    print(f"\nget_student_address: {get_student_address}\n")

    # Validate document info
    document_list = get_student_document_info.get("data", [])
    if not document_list:
        raise CustomApiException(ErrorCodes.NOT_FOUND, "Document info not found.")

    document_data = document_list[0]

    # Qualification decision: University > Lyceum > School
    diploma_data = get_diploma_info[0] if isinstance(get_diploma_info, list) and get_diploma_info else None

    lyceum_data = None
    if isinstance(get_lyceum_graduate.get("data"), dict):
        lyceum_data = get_lyceum_graduate["data"].get("student")

    school_data = get_e_shahodatnoma_info.get("data") if get_e_shahodatnoma_info.get("success") else None

    if diploma_data:
        qualification = 4  # University
        name_qualification = diploma_data.get("institution_name")
    elif lyceum_data:
        qualification = 3  # Lyceum
        name_qualification = lyceum_data.get("school")
    elif school_data:
        qualification = 1  # Middle School
        name_qualification = school_data.get("school")
    else:
        qualification = None
        name_qualification = None

    # Parse gender
    gender_code = document_data.get("sex")
    gender = 1 if gender_code == 1 else 2 if gender_code == 2 else None
    """
    Address API response format:
    example response:
    {
    "Data":{"PermanentRegistration":{"Cadastre":"12:08:05:01:07:0035",
    "Country":{"Id":182,"Value":"ЎЗБЕКИСТОН","IdValue":"(182) ЎЗБЕКИСТОН"},
    "Region":{"Id":12,"Value":"СИРДАРЁ ВИЛОЯТИ",
    "IdValue":"(12) СИРДАРЁ ВИЛОЯТИ"},
    "District":{"Id":1205,"Value":"ХОВОС ТУМАНИ",
    "IdValue":"(1205) ХОВОС ТУМАНИ"},
    "Maxalla":{"Id":3174,"Guid":"12080009",
    "Value":"КАЙИРМА МФЙ"},"Street":{"Id":48421,
    "Guid":"408-000374","Value":"МУРУВВАТ КУЧАСИ"},
    "Address":"Сырдарьинская область, Хавастский район, Кайирма (Богистон) МСГ, ул. Мурувват, дом 20","RegistrationDate":"2021-12-27T00:00:00"},
    "TemproaryRegistrations":null},"AnswereId":1,"AnswereMessage":"Ok","AnswereComment":""
    }
    """

    # Decode photo
    photo_base64 = document_data.get("photo")
    photo_file = None
    if photo_base64:
        try:
            photo_file = ContentFile(base64.b64decode(photo_base64), name=f"{pinfl}_photo.jpg")
        except Exception as e:
            print(f"Failed to decode photo: {e}")

    # Create Student
    student = Student.objects.create(
        user_id=user_id,
        first_name=document_data.get("namelat"),
        last_name=document_data.get("surnamelat"),
        father_name=document_data.get("patronymlat"),
        birth_date=document_data.get("birth_date"),
        birth_place=document_data.get("birthplace"),
        citizenship=document_data.get("citizenship"),
        address=get_student_address.get('Data', {}).get('PermanentRegistration', {}).get('Address', ''),
        pinfl=pinfl,
        passport_number=passport_number,
        gender=gender,
        qualification=qualification,
        name_qualification=name_qualification,
        photo=photo_file,
        is_registred=True,
    )

    return student