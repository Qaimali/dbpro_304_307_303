# Generated by Django 2.1.8 on 2019-04-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0012_auto_20190427_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registrationNumber',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
