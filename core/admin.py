from django.contrib import admin
from .models import Profile, Project, Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('assigned_to',)

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Task,TaskAdmin)
