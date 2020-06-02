from django.contrib import admin

from .models import Department, CourseType, Course, Alias, PrerequisiteData
# Register your models here.

admin.site.register(Department)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(Alias)
admin.site.register(PrerequisiteData)