from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models.user import User

QUALIFICATION_CHOICES = (
    (1, 'Middle School'),
    (2, 'College'),
    (3, 'Lyceum'),
    (4, 'University'),
    (5, 'Technical School'),
)
GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female')
)


class Student(SafeBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    additional_phone_number = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    citizenship = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pinfl = models.CharField(max_length=200, blank=True, null=True)
    passport_number = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="---", blank=True, null=True)
    qualification = models.IntegerField(choices=QUALIFICATION_CHOICES, blank=True, null=True)
    name_qualification = models.CharField(max_length=250, blank=True, null=True)
    diploma = models.FileField(upload_to='diplomas/', blank=True, null=True)
    photo = models.FileField(upload_to='photos/', blank=True, null=True)
    is_registred = models.BooleanField(default=False)
    is_attended_exam = models.BooleanField(default=False)
    is_exam_exempt = models.BooleanField(default=False)
    is_passed_exam = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = "Students"
        ordering = ['-user__created_datetime']


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
