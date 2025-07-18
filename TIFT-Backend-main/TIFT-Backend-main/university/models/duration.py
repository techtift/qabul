from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

class Duration(SafeBaseModel):
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='duration_faculties', verbose_name=_("Faculty"))
    study_type = models.ForeignKey('StudyType', on_delete=models.CASCADE, related_name='duration_study_types', verbose_name=_("Study Type"))
    study_duration = models.FloatField(verbose_name=_("Study Duration (years)"), null=True, blank=True)

    class Meta:
        verbose_name = _("Study Duration")
        verbose_name_plural = _("Study Durations")
        ordering = ['faculty']

    def __str__(self):
        return f"{self.study_duration} yil" if self.study_duration else "Noma'lum davomiylik"