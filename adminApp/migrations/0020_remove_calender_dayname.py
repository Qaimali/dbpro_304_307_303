# Generated by Django 2.1.8 on 2019-05-03 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0019_subjectclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calender',
            name='DayName',
        ),
    ]
