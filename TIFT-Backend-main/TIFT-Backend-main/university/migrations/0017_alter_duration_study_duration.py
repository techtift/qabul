# Generated by Django 5.1.3 on 2025-06-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0016_program_study_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duration',
            name='study_duration',
            field=models.FloatField(blank=True, null=True, verbose_name='Study Duration (years)'),
        ),
    ]
