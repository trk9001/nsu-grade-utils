from django import http
from django.db.models import Max
from django.urls import reverse, reverse_lazy
from django.views import generic

from . import forms, models


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        last_trimester_code = (
            student.trimesters
            .aggregate(last_trimester_code=Max('code'))
            .get('last_trimester_code', None)
        )
        if last_trimester_code:
            next_trimester_code = (
                last_trimester_code + 1
                if last_trimester_code % 10 < 3
                else (last_trimester_code // 10 + 1) * 10 + 1
            )
        else:
            next_trimester_code = None
        context['next_trimester_code'] = next_trimester_code
        data = {'student': student}
        trimester_form = forms.TrimesterCreateForm(initial=data)
        context['trimester_form'] = trimester_form
        return context


class TrimesterCreate(generic.View):
    """Handle POST requests for trimester creation."""

    http_method_names = ['post', 'put']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def post(self, request, **kwargs):
        action_type = request.POST.get('action-type')
        if action_type in ['add-first-trimester', 'add-next-trimester']:
            form = forms.TrimesterCreateForm(request.POST)
            if form.is_valid():
                self.object = form.save()
                return http.HttpResponseRedirect(
                    reverse(
                        'student-detail',
                        kwargs={'slug': kwargs.get('slug')}
                    )
                )
            else:
                return http.HttpResponseBadRequest
        else:
            return http.HttpResponseBadRequest

    def put(self, *args, **kwargs):
        self.post(*args, **kwargs)
