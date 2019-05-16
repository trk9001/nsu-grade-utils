from django.urls import path

from . import views

urlpatterns = [
    path(
        'students/',
        views.StudentList.as_view(),
        name='student-list',
    ),
    path(
        'students/new/',
        views.StudentCreate.as_view(),
        name='student-create',
    ),
]
