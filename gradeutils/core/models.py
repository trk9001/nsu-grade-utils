from decimal import Decimal
from typing import Iterable, Union

from django.core.validators import RegexValidator
from django.db import models


def qdecimal(value: Union[int, float, Decimal, str],
             exp: Decimal = Decimal('1.00')) -> Decimal:
    """Return a quantized Decimal form of x."""
    x = str(value) if isinstance(value, float) else value
    return Decimal(x).quantize(exp)


class Student(models.Model):
    """A student enrolled in a particular program."""

    PROGRAM_CHOICES = (
        ('CSE', 'Computer Science and Engineering'),
        ('EEE', 'Electrical and Electronic Engineering'),
        ('ETE', 'Electronics and Telecommunication Engineering'),
        ('BBT', 'Biochemistry & Biotechnology'),
        ('MIC', 'Microbiology'),
    )

    nsuid = models.CharField(
        max_length=7,
        verbose_name='NSU ID',
        help_text='<em>The first seven digits of your student ID</em>',
        validators=(
            RegexValidator(r'^\d{7}$', message='Should be a 7-digit number'),
        ),
    )
    program = models.CharField(
        max_length=5,
        choices=PROGRAM_CHOICES,
    )

    class Meta:
        ordering = ['nsuid']
        constraints = [
            models.UniqueConstraint(
                fields=['nsuid', 'program'],
                name='unique_student_program_pair',
            ),
        ]

    def __str__(self):
        return f'{self.nsuid}, {self.get_program_display()}'

    def course_list(self, max_trimester: int = None) -> models.QuerySet:
        """Flattened queryset of courses taken by the enrolled student."""
        if not max_trimester:
            return (Course.objects.filter(trimester__student=self)
                    .order_by('trimester__code'))
        else:
            return (Course.objects.filter(trimester__student=self)
                    .filter(trimester__code__lte=max_trimester)
                    .order_by('trimester__code'))

    @property
    def cumulative_grade_point_average(self) -> Decimal:
        """CGPA of the enrolled student (out of 4)."""
        courses: Iterable[Course] = self.course_list()
        cgpa_numerator = sum([
            course.credits * course.grade_point
            for course in courses
            if not course.retaken
            and course.grade_point
        ])
        cgpa_denominator = sum([
            course.credits
            for course in courses
            if not course.retaken
            and course.grade_point
        ])
        cgpa = (
            0 if cgpa_denominator.is_zero()
            else cgpa_numerator / cgpa_denominator
        )
        return qdecimal(cgpa)

    @property
    def cgpa(self) -> Decimal:
        """Alias of cumulative_grade_point_average."""
        return self.cumulative_grade_point_average


class Trimester(models.Model):
    """A trimester completed by an enrolled student."""

    student = models.ForeignKey(
        Student,
        related_name='trimesters',
        related_query_name='trimester',
        on_delete=models.CASCADE,
    )
    code = models.PositiveSmallIntegerField(
        help_text='<em>The numerical code of the trimester '
                  '(eg. 152 for the Summer 2015 trimester)</em>',
    )

    class Meta:
        order_with_respect_to = 'student'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'code'],
                name='unique_trimester_per_student',
            ),
        ]

    def __str__(self):
        return f'{self.code} ({self.student})'

    @property
    def grade_point_average(self) -> Decimal:
        """Grade point average in the trimester."""
        gpa_numerator = sum([
            course.credits * course.grade_point
            for course in self.courses
            if course.grade_point
        ])
        gpa_denominator = sum([
            course.credits
            for course in self.courses
            if course.grade_point
        ])
        gpa = (
            0 if gpa_denominator.is_zero()
            else gpa_numerator / gpa_denominator
        )
        return qdecimal(gpa)

    @property
    def gpa(self) -> Decimal:
        """Alias of grade_point_average."""
        return self.grade_point_average


class Course(models.Model):
    """A course taken by an enrolled student in a particular trimester."""

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
        help_text='<em>The course code (eg. MAT116)</em>',
        validators=(RegexValidator(r'^[A-Z]{3}\d{3}[ABILR]?$'),),
    )
    credits = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        default='F',
    )
    retaken = models.BooleanField(
        help_text=('<em>True if this course has been retaken '
                   'in a later trimester</em>'),
        default=False,
        editable=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['trimester', 'code'],
                name='unique_course_per_trimester',
            ),
        ]

    def __str__(self):
        return f'{self.code}, {self.trimester}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Mark all previous takes of this course as retaken
        takes: Iterable[Course] = Course.objects.filter(
            trimester__student=self.trimester.student,
            trimester__code__lt=self.trimester.code,
            code=self.code,
            retaken=False
        )
        for take in takes:
            take.retaken = True
            # Use the default save method instead of this (overridden) one in
            # order to avoid recursive saving
            super(Course, take).save(update_fields=['retaken'])

    @property
    def grade_point(self) -> Union[Decimal, None]:
        """Numerical point equivalent of the grade."""
        return self.map_grade_to_point(self.grade)

    @property
    def gp(self):
        """Alias of grade_point."""
        return self.grade_point

    @staticmethod
    def map_grade_to_point(grade: str) -> Union[Decimal, None]:
        """Map a grade string to a numerical grade point."""
        mapping = {
            'A': qdecimal(4.00),
            'A-': qdecimal(3.70),
            'B+': qdecimal(3.30),
            'B': qdecimal(3.00),
            'B-': qdecimal(2.70),
            'C+': qdecimal(2.30),
            'C': qdecimal(2.00),
            'C-': qdecimal(1.70),
            'D+': qdecimal(1.30),
            'D': qdecimal(1.00),
            'F': qdecimal(0.00),
            'W': None,
            'I': None
        }
        return mapping.get(grade, None)
