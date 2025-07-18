from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

class Subject(SafeBaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Subject Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Subject Description"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['name']

    def __str__(self):
        return self.name        