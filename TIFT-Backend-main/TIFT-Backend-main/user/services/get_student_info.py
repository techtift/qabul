from django.contrib.auth.hashers import make_password
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from core.utils import MyGovClient

my_gov_client = MyGovClient()

def get_student_info_service(pinfl):
    student_data = my_gov_client.get_student_info(pinfl)
    return student_data