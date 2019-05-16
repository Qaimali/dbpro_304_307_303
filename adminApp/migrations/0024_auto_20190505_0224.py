# Generated by Django 2.1.8 on 2019-05-04 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0023_auto_20190504_1326'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('Date', 'StudentId', 'SubjectId')},
        ),
        migrations.AlterUniqueTogether(
            name='subjectclass',
            unique_together={('ClassId', 'SubjectId', 'SemsterName')},
        ),
    ]
