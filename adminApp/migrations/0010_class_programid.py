# Generated by Django 2.1.8 on 2019-04-17 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0009_auto_20190416_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='ProgramId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminApp.Program'),
            preserve_default=False,
        ),
    ]
