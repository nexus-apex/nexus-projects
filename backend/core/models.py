from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("planning", "Planning"), ("active", "Active"), ("on_hold", "On Hold"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="planning")
    priority = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="low")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255, blank=True, default="")
    assignee = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("to_do", "To Do"), ("in_progress", "In Progress"), ("review", "Review"), ("done", "Done")], default="to_do")
    priority = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="low")
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.IntegerField(default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class TimeEntry(models.Model):
    task_name = models.CharField(max_length=255)
    member = models.CharField(max_length=255, blank=True, default="")
    hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)
    billable = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.task_name
