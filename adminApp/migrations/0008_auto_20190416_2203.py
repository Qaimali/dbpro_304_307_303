# Generated by Django 2.1.8 on 2019-04-16 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0007_auto_20190416_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='DepartmentId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department'),
        ),
    ]
