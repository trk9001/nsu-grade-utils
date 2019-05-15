import nested_admin
from django.contrib import admin

from . import models

admin.site.site_header = 'NSU Grade Utils - Admin'
admin.site.site_title = 'NSU Grade Utils'
admin.site.index_title = 'Admin'


class CourseInline(nested_admin.NestedTabularInline):
    model = models.Course
    fields = ['code', 'credits', 'grade']
    extra = 0


class TrimesterInline(nested_admin.NestedStackedInline):
    model = models.Trimester
    inlines = [CourseInline]
    fields = ['code']
    sortable_field_name = 'code'
    extra = 0


class StudentAdmin(nested_admin.NestedModelAdmin):
    fields = ['nsuid', 'program']
    inlines = [TrimesterInline]


admin.site.register(models.Student, StudentAdmin)
