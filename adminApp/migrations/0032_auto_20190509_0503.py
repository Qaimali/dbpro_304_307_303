# Generated by Django 2.1.8 on 2019-05-09 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0031_auto_20190509_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='DepartmentId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department', verbose_name='Department'),
        ),
    ]