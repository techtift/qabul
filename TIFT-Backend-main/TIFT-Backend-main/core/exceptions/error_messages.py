from enum import Enum
from rest_framework import status

class ErrorCodes(Enum):
    UNAUTHORIZED = 'unauthorized'
    INVALID_INPUT = 'invalid_input'
    FORBIDDEN = 'forbidden'
    NOT_FOUND = 'not_found'
    ALREADY_EXISTS = 'already_exists'
    USER_DOES_NOT_EXIST = 'user_does_not_exist'
    INCORRECT_PASSWORD = 'incorrect_password'
    INVALID_TOKEN = 'invalid_token'
    EXPIRED_TOKEN = 'expired_token'
    VALIDATION_FAILED = 'validation_failed'
    USER_BLOCKED = 'user_blocked'
    PERMISSION_DENIED = 'permission_denied'
    EXPIRED_OTP = 'expired_otp'
    NOT_CONFIRMED = 'not_confirmed'
    NOT_VERIFIED = 'not_verified'
    SMS_NOT_SENT = 'sms_not_sent'
    TIMEOUT = 'timeout'

ERROR_MESSAGES = {
    ErrorCodes.UNAUTHORIZED: {
        "message": "Unauthorized access.",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    ErrorCodes.INVALID_INPUT: {
        "message": "Invalid input provided.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.FORBIDDEN: {
        "message": "Permission denied.",
        "status": status.HTTP_403_FORBIDDEN,
    },
    ErrorCodes.NOT_FOUND: {
        "message": "Resource not found.",
        "status": status.HTTP_404_NOT_FOUND,
    },
    ErrorCodes.ALREADY_EXISTS: {
        "message": "Resource already exists.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.USER_DOES_NOT_EXIST: {
        "message": "User does not exist.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.INCORRECT_PASSWORD: {
        "message": "Incorrect password.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.INVALID_TOKEN: {
        "message": "Invalid token provided.",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    ErrorCodes.EXPIRED_TOKEN: {
        "message": "Token has expired.",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
    ErrorCodes.VALIDATION_FAILED: {
        "message": "Validation failed for the provided input.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.USER_BLOCKED: {
        "message": "User account is blocked.",
        "status": status.HTTP_403_FORBIDDEN,
    },
    ErrorCodes.PERMISSION_DENIED: {
        "message": "You do not have permission to perform this action.",
        "status": status.HTTP_403_FORBIDDEN,
    },
    ErrorCodes.EXPIRED_OTP: {
        "message": "OTP has expired.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.NOT_CONFIRMED: {
        "message": "User account is not confirmed.",
        "status": status.HTTP_403_FORBIDDEN,
    },
    ErrorCodes.NOT_VERIFIED: {
        "message": "User account is not verified.",
        "status": status.HTTP_403_FORBIDDEN,
    },
    ErrorCodes.SMS_NOT_SENT: {
        "message": "SMS could not be sent.",
        "status": status.HTTP_400_BAD_REQUEST,
    },
    ErrorCodes.TIMEOUT: {
        "message": "Request timed out. Please try again later.",
        "status": status.HTTP_408_REQUEST_TIMEOUT,
    },
   }

def get_error_details(error_code: ErrorCodes):
    return ERROR_MESSAGES.get(
        error_code,
        {"message": "An unknown error occurred.", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
    )


class ClickErrorCode(Enum):
    ClickRequestError = (-8, 'Error in request from click')
    AlreadyPaidError = (-4, 'Already paid')
    SignCheckFailedError = (-1, 'SIGN CHECK FAILED!')
    UserNotFound = (-5, 'User does not exist')
    TransactionError = (-9, 'Transaction cancelled')
    IncorrectParameterAmount = (-2, 'Incorrect parameter amount')
    TransactionNotExist = (-6, 'Transaction does not exist')
    ActionNotFound = (-3, 'Action not found')