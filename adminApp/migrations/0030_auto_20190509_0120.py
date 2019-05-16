# Generated by Django 2.1.8 on 2019-05-08 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0029_auto_20190508_2304'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classsection',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='classsection',
            name='ClassId',
        ),
        migrations.RemoveField(
            model_name='classsection',
            name='SectionId',
        ),
        migrations.RemoveField(
            model_name='result',
            name='ExamId',
        ),
        migrations.RemoveField(
            model_name='result',
            name='classSectionId',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='StudentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Student', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='SubjectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Subject', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='class',
            name='DepartmentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='class',
            name='ProgramId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Program', verbose_name='Program'),
        ),
        migrations.AlterField(
            model_name='department',
            name='InstitueId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Institue', verbose_name='Institute'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='ExamId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Exam', verbose_name='Exam'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='StudentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Student', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='ClassId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Class', verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='DepartmentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='SectionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='SubjectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Subject', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='fine',
            name='personId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Person', verbose_name='Person'),
        ),
        migrations.AlterField(
            model_name='program',
            name='DepartmentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='DepartmentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminApp.Department', verbose_name='Department'),
        ),
        migrations.DeleteModel(
            name='classSection',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
    ]
