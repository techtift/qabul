from modeltranslation.translator import translator, TranslationOptions
from university.models.application import Application
from university.models.faculty import Faculty
from university.models.program import Program
from university.models.subject import Subject
from university.models.study_type import StudyType
from university.models.exam_type import ExamType

class ApplicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class FacultyTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class ProgramTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class SubjectTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class StudyTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class ExamTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Application, ApplicationTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(Program, ProgramTranslationOptions)
translator.register(Subject, SubjectTranslationOptions)
translator.register(StudyType, StudyTypeTranslationOptions)
translator.register(ExamType, ExamTypeTranslationOptions)