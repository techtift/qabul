# Generated by Django 5.1.3 on 2025-06-29 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0019_studytypefaculty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studytypefaculty',
            options={'verbose_name': 'Study Type Faculty', 'verbose_name_plural': 'Study Type Faculties'},
        ),
    ]
