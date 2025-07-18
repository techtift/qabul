
from core.models.basemodel import SafeBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from university.models.program import Program
from university.models.faculty import Faculty
from university.models.study_type import StudyType
from university.models.exam import Exam
from user.models.student import Student
from university.models.exam_type import ExamType

class Application(SafeBaseModel):
    title = models.CharField(max_length=100, verbose_name=_("Application Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Application Description"))
    programs = models.ManyToManyField(Program, related_name="application_set", verbose_name=_("Programs"))
    faculties = models.ManyToManyField(Faculty, related_name="application_set", verbose_name=_("Faculties"))
    study_types = models.ManyToManyField(StudyType, related_name="application_studytypes", verbose_name=_("Study Types"))
    exams = models.ManyToManyField(Exam, related_name="application_exams", verbose_name=_("Exams"), blank=True, null=True)
    exam_types = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name="application_exam_types", verbose_name=_("Exam Type"), blank=True, null=True)
    start_date = models.DateTimeField(verbose_name=_("Start Date"))
    end_date = models.DateTimeField(verbose_name=_("End Date"))

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        ordering = ['start_date']

    def __str__(self):
        return self.title

class StudentApplication(SafeBaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications", verbose_name=_("Student"))
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="student_list")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="student_applications")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="student_applications", null=True, blank=True)
    study_type = models.ForeignKey(StudyType, on_delete=models.CASCADE, related_name="student_applications", null=True, blank=True)
    is_online_exam = models.BooleanField(default=False, verbose_name=_("Is Online Exam"))
    exam_date = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="student_exam_applications", blank=True, null=True)
    exam_result = models.CharField(max_length=20, blank=True, null=True)
    # Transfer-specific fields
    is_transfer = models.BooleanField(default=False)
    transfer_level = models.IntegerField(blank=True, null=True)
    transcript = models.FileField(upload_to='transcripts/', blank=True, null=True)
    score = models.FloatField(blank=True, null=True, verbose_name=_("Score"))
    lang = models.CharField(max_length=20, choices=[
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
    ], default='uz', verbose_name=_("Language"))

    class Meta:
        verbose_name = _("Student Application")
        verbose_name_plural = _("Student Applications")

    def __str__(self):
        return f"{self.student} - {self.program.name}"