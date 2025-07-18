from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from university.models.program import Program
from university.models.subject import Subject


class Faculty(SafeBaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='faculties', verbose_name=_("Program"))
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Faculty Code"), null=True, blank=True)
    day_price = models.TextField(verbose_name=_("Day Price"), null=True, blank=True)  # Assuming day_price is a string for flexibility
    night_price = models.TextField(verbose_name=_("Night Price"), null=True, blank=True)  # Assuming night_price is a string for flexibility
    external_price = models.TextField(verbose_name=_("External Price"), null=True, blank=True) # Assuming external_price is a string for flexibility
    name = models.CharField(max_length=100, verbose_name=_("Faculty Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Faculty Description"))
    subjects = models.ManyToManyField(Subject, related_name='faculty_subjects', verbose_name=_("Subjects"), blank=True)

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")
        ordering = ['name']

    def __str__(self):
        return self.name