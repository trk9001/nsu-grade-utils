# Generated by Django 2.2.1 on 2019-05-15 17:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='<em>The course code (eg. MAT116)</em>', max_length=4, validators=[django.core.validators.RegexValidator('^[A-Z]{3}\\d{3}[ABILR]?$')])),
                ('credits', models.DecimalField(decimal_places=1, max_digits=2)),
                ('grade', models.CharField(choices=[('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D+', 'D+'), ('D', 'D'), ('F', 'F'), ('W', 'W'), ('I', 'I')], default='F', max_length=2)),
                ('retaken', models.BooleanField(default=False, editable=False, help_text='<em>True if this course has been retaken in a later trimester</em>')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsuid', models.CharField(help_text='<em>The first seven digits of your student ID</em>', max_length=7, validators=[django.core.validators.RegexValidator('^\\d{7}$', message='Should be a 7-digit number')], verbose_name='NSU ID')),
                ('program', models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('EEE', 'Electrical and Electronic Engineering'), ('ETE', 'Electronics and Telecommunication Engineering'), ('BBT', 'Biochemistry & Biotechnology'), ('MIC', 'Microbiology')], max_length=5)),
            ],
            options={
                'ordering': ['nsuid'],
            },
        ),
        migrations.CreateModel(
            name='Trimester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveSmallIntegerField(help_text='<em>The numerical code of the trimester (eg. 152 for the Summer 2015 trimester)</em>')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trimesters', related_query_name='trimester', to='core.Student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.UniqueConstraint(fields=('nsuid', 'program'), name='unique_student_program_pair'),
        ),
        migrations.AddField(
            model_name='course',
            name='trimester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', related_query_name='course', to='core.Trimester'),
        ),
        migrations.AddConstraint(
            model_name='trimester',
            constraint=models.UniqueConstraint(fields=('student', 'code'), name='unique_trimester_per_student'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='trimester',
            order_with_respect_to='student',
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('trimester', 'code'), name='unique_course_per_trimester'),
        ),
    ]
