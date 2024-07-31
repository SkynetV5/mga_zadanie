from django.contrib import admin

from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_filter = ("name", "status","assigned_user")
    list_display = ("name", "status","assigned_user")


admin.site.register(Task, TaskAdmin)