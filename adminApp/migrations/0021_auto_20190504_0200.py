# Generated by Django 2.1.8 on 2019-05-03 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0020_remove_calender_dayname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calender',
            name='date_Time',
            field=models.DateField(),
        ),
    ]
