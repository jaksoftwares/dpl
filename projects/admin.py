from django.contrib import admin
from .models import Project, Task, Reminder

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ReminderInline(admin.TabularInline):
    model = Reminder
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'client', 'status', 'progress_display', 'deadline', 'is_overdue_display')
    list_filter = ('status', 'owner')
    search_fields = ('name', 'client', 'description')
    inlines = [TaskInline, ReminderInline]
    
    def progress_display(self, obj):
        return f"{obj.progress:.1f}%"
    progress_display.short_description = 'Progress'

    def is_overdue_display(self, obj):
        return obj.is_overdue
    is_overdue_display.boolean = True
    is_overdue_display.short_description = 'Overdue'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'due_date')
    list_filter = ('status', 'project__owner')
    search_fields = ('title', 'project__name')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('project', 'reminder_date', 'is_sent')
    list_filter = ('is_sent', 'project__owner')
