from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Project, Task, TimeEntry
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusProjects with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusprojects.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Project.objects.count() == 0:
            for i in range(10):
                Project.objects.create(
                    name=f"Sample Project {i+1}",
                    client=f"Sample {i+1}",
                    status=random.choice(["planning", "active", "on_hold", "completed", "cancelled"]),
                    priority=random.choice(["low", "medium", "high", "critical"]),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 90)),
                    budget=round(random.uniform(1000, 50000), 2),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Project records created'))

        if Task.objects.count() == 0:
            for i in range(10):
                Task.objects.create(
                    title=f"Sample Task {i+1}",
                    project_name=f"Sample Task {i+1}",
                    assignee=f"Sample {i+1}",
                    status=random.choice(["to_do", "in_progress", "review", "done"]),
                    priority=random.choice(["low", "medium", "high"]),
                    due_date=date.today() - timedelta(days=random.randint(0, 90)),
                    estimated_hours=random.randint(1, 100),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Task records created'))

        if TimeEntry.objects.count() == 0:
            for i in range(10):
                TimeEntry.objects.create(
                    task_name=f"Sample TimeEntry {i+1}",
                    member=f"Sample {i+1}",
                    hours=round(random.uniform(1000, 50000), 2),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    billable=random.choice([True, False]),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 TimeEntry records created'))
