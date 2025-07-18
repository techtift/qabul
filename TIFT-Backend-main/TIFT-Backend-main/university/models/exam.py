from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from university.models.program import Program
from university.models.faculty import Faculty


class Exam(SafeBaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exam_programs', null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='exam_faculties', null=True, blank=True)
    is_online = models.BooleanField(default=False, verbose_name=_("Is Online Exam"))
    exam_date = models.DateTimeField()

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return f"{self.exam_date} - {self.is_online} - {self.program.name if self.program else 'No Program'} - {self.faculty.name if self.faculty else 'No Faculty'}"