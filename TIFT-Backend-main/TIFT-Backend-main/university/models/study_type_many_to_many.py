from core.models.basemodel import SafeBaseModel
from university.models.study_type import StudyType
from university.models.faculty import Faculty
from university.models.program import Program
from django.utils.translation import gettext_lazy as _

from django.db import models


class StudyTypeFaculty(SafeBaseModel):
    study_type = models.ManyToManyField(StudyType, related_name='study_type_faculties',
                                        verbose_name=_("Study Type Name"))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty_study_types',
                                verbose_name=_("Faculty Name"))
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_study_types',
                                verbose_name=_("Program Name"))

    def __str__(self):
        return f"{self.study_type} - {self.faculty} - {self.program}"

    class Meta:
        verbose_name = _("Study Type Faculty")
        verbose_name_plural = _("Study Type Faculties")
