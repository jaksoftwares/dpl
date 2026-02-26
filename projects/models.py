from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count, Q

class Project(models.Model):
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    progress = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-deadline']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            old_project = Project.objects.get(pk=self.pk)
            if self.status == 'COMPLETED' and old_project.status != 'COMPLETED':
                self.completed_at = timezone.now()
            elif self.status != 'COMPLETED' and old_project.status == 'COMPLETED':
                self.completed_at = None
        elif self.status == 'COMPLETED':
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.deadline < timezone.now().date() and self.status != 'COMPLETED':
            return True
        return False

    def update_progress(self):
        """
        Recalculates progress based on tasks. 
        If no tasks exist, progress remains as manually set or default 0.
        """
        tasks = self.tasks.all()
        if tasks.exists():
            done_tasks = tasks.filter(status='DONE').count()
            total_tasks = tasks.count()
            self.progress = (done_tasks / total_tasks) * 100
        
        # Status automation
        if self.progress >= 100:
            if self.status != 'COMPLETED':
                self.completed_at = timezone.now()
            self.status = 'COMPLETED'
        elif self.progress > 0 and self.status == 'NOT_STARTED':
            self.status = 'IN_PROGRESS'
            self.completed_at = None
        elif self.progress < 100 and self.status == 'COMPLETED':
            self.status = 'IN_PROGRESS'
            self.completed_at = None
            
        self.save()

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Recalculate project progress
        self.project.update_progress()

    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        project.update_progress()

class Reminder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.project.name} on {self.reminder_date}"

    @property
    def is_overdue(self):
        return self.reminder_date < timezone.now().date() and not self.is_sent
