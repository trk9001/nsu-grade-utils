from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='index',
    ),
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
    path(
        'students/<slug:slug>/',
        views.StudentDetail.as_view(),
        name='student-detail',
    ),
    path(
        'students/<slug:slug>/new-trimester/',
        views.TrimesterCreate.as_view(),
        name='trimester-create',
    ),
]
