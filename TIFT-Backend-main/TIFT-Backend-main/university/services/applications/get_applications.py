from university.models.application import Application
from core.exceptions.exception import CustomApiException
from core.exceptions.error_messages import ErrorCodes
from django.utils import timezone


def get_applications(application_id=None, only_valid=False):
    now = timezone.now()

    if application_id:
        application = Application.objects.filter(id=application_id).first()
        if not application:
            raise CustomApiException(
                ErrorCodes.NOT_FOUND,
                "Application with the given ID does not exist."
            )
        return application
    else:
        # Only fetch valid applications if requested
        qs = Application.objects.all()
        if only_valid:
            qs = qs.filter(start_date__lte=now, end_date__gte=now)
        return qs