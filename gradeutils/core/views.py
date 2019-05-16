from django.views.generic import ListView

from . import models


class StudentList(ListView):
    """Render a list of Student references."""

    model = models.Student
    template_name = 'core/student_list.html'
