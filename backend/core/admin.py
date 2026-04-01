from django.contrib import admin
from .models import Project, Task, TimeEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "client", "status", "priority", "start_date", "created_at"]
    list_filter = ["status", "priority"]
    search_fields = ["name", "client"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project_name", "assignee", "status", "priority", "created_at"]
    list_filter = ["status", "priority"]
    search_fields = ["title", "project_name", "assignee"]

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ["task_name", "member", "hours", "date", "billable", "created_at"]
    search_fields = ["task_name", "member"]
