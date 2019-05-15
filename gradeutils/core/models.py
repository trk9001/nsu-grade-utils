from django.db import models
from django.core.validators import RegexValidator


class Student(models.Model):

    id = models.CharField(
        max_length=7,
        verbose_name='ID',
        help_text='<em>The first seven digits of your student ID</em>',
        validators=(RegexValidator(r'^\d{7}$'),),
        primary_key=True,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Student #{self.id}'


class Trimester(models.Model):

    student = models.ForeignKey(
        Student,
        related_name='trimesters',
        related_query_name='trimester',
        on_delete=models.CASCADE,
    )
    code = models.PositiveSmallIntegerField(
        help_text='<em>The numerical code of the trimester'
                  '(eg. 152 for the Summer 2015 trimester)</em>',
    )

    class Meta:
        unique_together = ('student', 'code')  # TODO: Use UniqueConstraint
        order_with_respect_to = 'student'

    def __str__(self):
        return f'{self.code} ({self.student.id})'


class Course(models.Model):

    GRADE_CHOICES = (
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
        ('W', 'W'),
        ('I', 'I'),
    )

    trimester = models.ForeignKey(
        Trimester,
        related_name='courses',
        related_query_name='course',
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=4,
        validators=(RegexValidator(r'^[A-Z]{3}\d{3}[ABILR]?$'),),
    )
    credits = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
    )
