from datetime import timedelta, date
import calendar
from django.utils.translation import gettext_lazy as _
from requests.auth import HTTPBasicAuth
import requests
import environ
from pathlib import Path
from django.core.cache import cache
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / ".env")

BASE_URL = env.str("BASE_URL", default="http://localhost:8000")
SMS_API_USERNAME = env.str("SMS_API_USERNAME", default="username")
SMS_API_PASSWORD = env.str("SMS_API_PASSWORD", default="password")
SMS_API_ORGINATOR = env.str("SMS_API_ORGINATOR", default="YourSenderName")  # SEND ID bu yerda
TOKEN = env.str("BOT_TOKEN",default="BOT_TOKEN")
ADMINS_ID=env.str("ADMINS_ID",default="").split(",")
import base64
from typing import Optional

class MyGovClient:
    def __init__(self):
        self.username = env.str("MYGOV_USERNAME")
        self.password = env.str("MYGOV_PASSWORD")
        self.consumer_key = env.str("MYGOV_CONSUMER_KEY")
        self.consumer_secret = env.str("MYGOV_CONSUMER_SECRET")

        self.auth_url = env.str("MYGOV_AUTH_URL")
        self.address_url = env.str("MYGOV_ADDRESS_API_URL")
        self.document_url = env.str("MYGOV_DOCUMENT_API_URL")
        self.lyceum_url = env.str("MYGOV_LYCEUM_GRADUATE_API_URL")
        self.diploma_url = env.str("MYGOV_DIMPLOMA_API_URL")
        self.eshahodatnoma_url = env.str("MYGOV_E_SHAHODATNOMA_API_URL")

        self.token: Optional[str] = None

    def get_token(self) -> str:
        auth = f"{self.consumer_key}:{self.consumer_secret}"
        auth_b64 = base64.b64encode(auth.encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_b64}",
        }

        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }

        response = requests.post(self.auth_url, headers=headers, data=data)
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def get_headers(self) -> dict:
        if not self.token:
            self.get_token()

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _post_with_refresh(self, url: str, payload: dict) -> dict:
        headers = self.get_headers()
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 401:
            # Token might have expired
            self.get_token()
            headers = self.get_headers()
            response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()
        return response.json()

    def get_student_address(self, pinfl: str) -> dict:
        return self._post_with_refresh(self.address_url, {"pinpp": pinfl})

    def get_document_info(self, birth_date: str, passport_number: str) -> dict:
        headers = self.get_headers()
        payload = {
            "transaction_id": 1,
            "is_consent": "Y",
            "sender_pinfl": 30907896610010,
            "langId": 1,
            "document": passport_number,
            "birth_date": birth_date,
            "is_photo": "Y",
            "Sender": "P",
        }
        response = requests.post(self.document_url, headers=headers, json=payload)

        if response.status_code == 401:
            self.get_token()
            headers = self.get_headers()
            response = requests.post(self.document_url, headers=headers, json=payload)

        response.raise_for_status()
        return response.json()

    def get_lyceum_graduate(self, pinfl: str) -> dict:
        return self._post_with_refresh(self.lyceum_url, {"pinfl": pinfl})

    def get_diploma_info(self, pinfl: str) -> dict:
        return self._post_with_refresh(self.diploma_url, {"pinfl": pinfl})

    def get_e_shahodatnoma_info(self, pinfl: str) -> dict:
        payload = {
            "pinfl": pinfl,
            "transaction_id": "1",
            "sender_pinfl": pinfl,
            "purpose": "3",
            "consent": "yes",
        }
        return self._post_with_refresh(self.eshahodatnoma_url, payload)

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

    """
    DOCUMENT API response format:
    example response:
    {
        "result":"1","data":[
        {"transaction_id":1,"current_pinpp":"50208046440023",
        "pinpps":["50208046440023"],"current_document":"AD0950895",
        "documents":[{"document":"AD0950895","type":"IDMS_RECV_MVD_IDCARD_CITIZEN",
        "docgiveplace":"ХАВАСТСКИЙ РОВД СЫРДАРЬИНСКОЙ ОБЛАСТИ",
        "docgiveplaceid":24255,"datebegin":"2021-12-27","dateend":"2031-12-26","status":2},
        {"document":"I-SR0006664","type":"IDMS_RECV_MJ_BIRTH_CERTS","docgiveplace":"ОТДЕЛ ЗАГС №1 ХАВАСТСКОГО РАЙОН‎А",
        "docgiveplaceid":739002118,"datebegin":"2004-08-06","dateend":null,"status":2},{"document":"FB0493211",
        "type":"IDMS_RECV_IP_DOCUMENTS","docgiveplace":"ХАВАСТСКИЙ РОВД СЫРДАРЬИНСКОЙ ОБЛАСТИ",
        "docgiveplaceid":24255,"datebegin":"2024-12-06","dateend":"2029-12-05","status":2}],
        "surnamelat":"ABDURAIMOV","namelat":"NODIRJON","patronymlat":"VALIJON O‘G‘LI",
        "birth_date":"2004-08-02","birthplace":"YANGIYER SHAHRI","birthcountry":"УЗБЕКИСТАН",
        "birthcountryid":182,"livestatus":1,"nationality":"УЗБЕК/УЗБЕЧКА","nationalityid":44,
        "citizenship":"УЗБЕКИСТАН","citizenshipid":182,"sex":1,"photo":"/9j/4AAQSkZJRgABAQEAYABgAAD/2wB2Q=="}],"comments":""
    }
    """

    """
    Lyceum Graduate API response format:
    example response:
    {
        "success": 200,
        "name": "Get Lyceum Graduate Data",
        "message": null,
        "code": 0,
        "data": {
            "current_time": 1709699696,
            "is_from_cache": false,
            "is_from_database": true,
            "cache_last_updated_time": 1682881200,
            "student": {
                "pinfl": "**********",
                "school_region_id": 15,
                "school_region": "Toshkent shahri",
                "school_district_id": 172,
                "school_district": "Yakkasaroy tumani",
                "school_id": 10776,
                "school": "Toshkent davlat pedagogika universiteti akademik litseyi",
                "year_of_graduation": 2024,
                "edu_type_id": 1,
                "edu_type_name": "lyceum"
            }
        }
    }
    """

    """
    Diploma API response format:
    example response:
    [
        {
            "id": 2297654,
            "pinfl": "3080895********",
            "edu_type_id": 3,
            "edu_type_name": "Oliy ta'lim",
            "institution_type_id": 2,
            "institution_type_name": "Universitet",
            "institution_id": 113,
            "institution_name": "Toshkent axborot texnologiyalari universiteti",
            "institution_old_name_id": 108,
            "institution_old_name": "Toshkent axborot texnologiyalari universiteti",
            "degree_id": 3,
            "degree_name": "Magistratura",
            "edu_form_id": 5,
            "edu_form_name": "Kunduzgi",
            "speciality_id": 42234,
            "speciality_old_id": null,
            "speciality_name": "Axborot xavfsizligi (yo‘nalishlar bo‘yicha)",
            "speciality_code": "5A330302",
            "edu_duration_id": null,
            "edu_duration_name": " yil",
            "edu_starting_date": null,
            "edu_finishing_date": null,
            "diploma_given_date": "2022-07-21",
            "diploma_serial_id": 9,
            "diploma_serial": "M",
            "diploma_number": "00032123",
            "diploma_type_id": 0,
            "diploma_type_name": "Oddiy diplom",
            "status_id": 8,
            "status_name": "Tasdiqlangan (Noto'liq)"
        }
    ]
    """

    """
    E-Shahodatnoma API response format:
    Example response:
    {
    "data": {
        "gradYear": 2023,
        "classLevel": "11-sinf",
        "certType": 3,
        "certTypeName": "Oddiy",
        "certSN": "UM 0******0",
        "firstName": "*******",
        "lastName": "******",
        "patronymic": "***** ****",
        "birthDate": "****-**-**T00:00:00",
        "pin": "*************",
        "iDocType": 5,
        "iDocTypeName": "ID karta",
        "iDocSerial": "**",
        "iDocNumber": "******",
        "regionId": 12,
        "region": "Toshkent shahar",
        "districtId": 621,
        "district": "Yakkasaroy tumani",
        "schoolId": 9720,
        "school": "26-sonli umumiy o'rta ta'lim maktabi",
        "grades6YearsAvg": 4.72
    },
    "success": true
    }
    """



def get_sms_token(force_refresh=False) -> str:
    token = cache.get("eskiz_token")
    if token and not force_refresh:
        return token

    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": SMS_API_USERNAME,
        "password": SMS_API_PASSWORD,
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token = response.json()["data"]["token"]
        cache.set("eskiz_token", token, timeout=60 * 60 * 5)  # cache for 5 hours
        return token
    raise CustomApiException(
        ErrorCodes.INVALID_INPUT,
        message=_("SMS API token olishda xatolik yuz berdi."),
    )

def send_sms_message(phone: str, message: str) -> dict:
    """
    Sends SMS using Eskiz. If token expired, auto-refreshes.
    """
    token = get_sms_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "mobile_phone": phone,
        "message": message,
        "from": SMS_API_ORGINATOR,
    }

    url = f"{BASE_URL}/message/sms/send"

    response = requests.post(url, headers=headers, json=data)

    # Handle expired token (401)

    if response.status_code == 401:
        token = get_sms_token(force_refresh=True)
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(url, headers=headers, json=data)

    return response


def get_date_range(from_date: date = None, to_date: date = None, daily: bool = False, weekly: bool = False, monthly: bool = False):
    today = date.today()

    if from_date is not None and to_date is not None:
        return from_date, to_date

    if daily:
        return today, today

    elif weekly:
        start_of_week = today - timedelta(days=today.weekday())  
        end_of_week = start_of_week + timedelta(days=6)          
        return start_of_week, end_of_week

    elif monthly:
        first_day = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_of_month = today.replace(day=last_day)
        return first_day, end_of_month

    first_day = today.replace(day=1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    end_of_month = today.replace(day=last_day)
    return first_day, end_of_month


