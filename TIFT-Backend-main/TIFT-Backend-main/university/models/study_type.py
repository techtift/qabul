from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

class StudyType(SafeBaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Study Type Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Study Type Description"))

    class Meta:
        verbose_name = _("Study Type")
        verbose_name_plural = _("Study Types")
        ordering = ['name']

    def __str__(self):
        return self.name
    