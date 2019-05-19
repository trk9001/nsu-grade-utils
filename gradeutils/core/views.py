from django.urls import reverse_lazy
from django.views import generic

from . import models


class Index(generic.RedirectView):
    """Redirect Index view to StudentList view."""

    pattern_name = 'student-list'


class StudentList(generic.ListView):
    """Render a list of Student references."""

    model = models.Student
    template_name = 'core/student_list.html'


class StudentCreate(generic.CreateView):
    """Render a form for a Student's creation."""

    model = models.Student
    fields = ['nsuid', 'program']
    template_name = 'core/student_create.html'
    success_url = reverse_lazy('student-list')


class StudentDetail(generic.DetailView):
    """Render the details of a Student."""

    model = models.Student
    template_name = 'core/student_detail.html'
