from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from university.models.subject import Subject

class Question(SafeBaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', verbose_name=_("Subject"))
    question_text = models.TextField(verbose_name=_("Question Text"))
    version_a = models.TextField(blank=True, null=True, verbose_name=_("Version A"))
    version_b = models.TextField(blank=True, null=True, verbose_name=_("Version B"))
    version_c = models.TextField(blank=True, null=True, verbose_name=_("Version C"))
    version_d = models.TextField(blank=True, null=True, verbose_name=_("Version D"))

    is_correct_a = models.BooleanField(default=False, verbose_name=_("Is Correct A"))
    is_correct_b = models.BooleanField(default=False, verbose_name=_("Is Correct B"))
    is_correct_c = models.BooleanField(default=False, verbose_name=_("Is Correct C"))
    is_correct_d = models.BooleanField(default=False, verbose_name=_("Is Correct D"))

    lang = models.CharField(max_length=10, choices=[
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
    ], default='uz', verbose_name=_("Language"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['subject', 'question_text']
    def __str__(self):
        return f"{self.subject.name} - {self.question_text[:50]}..." if self.question_text else f"{self.subject.name} - No Question Text"