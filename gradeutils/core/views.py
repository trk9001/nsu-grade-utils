from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from . import models


class StudentList(ListView):
    """Render a list of Student references."""

    model = models.Student
    template_name = 'core/student_list.html'


class StudentCreate(CreateView):
    """Render a form for a Student's creation."""

    model = models.Student
    fields = ['nsuid', 'program']
    template_name = 'core/student_create.html'
    success_url = reverse_lazy('student-list')
