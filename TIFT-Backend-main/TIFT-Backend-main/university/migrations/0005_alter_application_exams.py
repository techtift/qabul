# Generated by Django 5.1.3 on 2025-05-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0004_remove_subject_faculty_faculty_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='exams',
            field=models.ManyToManyField(blank=True, null=True, related_name='application_exams', to='university.exam', verbose_name='Exams'),
        ),
    ]
