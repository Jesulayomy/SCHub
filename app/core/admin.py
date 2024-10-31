"""Admin panel configuration for core application"""

from django.contrib import admin

from .models import (
    User,
    Student,
    Teacher,
    Parent,
)


admin.site.header = "Schub Admin Panel"
admin.site.site_header = "Schub Admin Panel"
admin.site.site_title = "Schub Admin Panel"

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
