# Generated by Django 2.1.8 on 2019-05-07 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0027_auto_20190507_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='Result',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='ExamId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminApp.Exam'),
            preserve_default=False,
        ),
    ]
