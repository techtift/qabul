from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Program(SafeBaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Program Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Program Description"))
    study_duration = models.IntegerField(verbose_name=_("Study Duration (years)"), null=True, blank=True)
    study_types=models.ManyToManyField('StudyType', related_name='program_study_types', verbose_name=_("Study Types"))
    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['name']

    def __str__(self):
        return self.name