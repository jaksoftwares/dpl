from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

from .models import Project, Task, Reminder

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        base_qs = Project.objects.filter(owner=user)
        
        today = timezone.now().date()
        next_week = today + timedelta(days=7)

        context['total_projects'] = base_qs.count()
        context['active_projects'] = base_qs.filter(status='IN_PROGRESS').count()
        context['completed_projects'] = base_qs.filter(status='COMPLETED').count()
        
        # Overdue logic
        context['overdue_projects'] = base_qs.filter(
            deadline__lt=today
        ).exclude(status='COMPLETED').count()

        # Upcoming deadlines (within 7 days)
        context['upcoming_deadlines'] = base_qs.filter(
            deadline__range=[today, next_week]
        ).exclude(status='COMPLETED')

        # Recent activities or summary can be added here
        return context

# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        queryset = Project.objects.filter(owner=self.request.user).select_related('owner')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(client__icontains=query) | Q(description__icontains=query)
            )
        return queryset

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).prefetch_related('tasks', 'reminders')

class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ['name', 'client', 'description', 'start_date', 'deadline', 'status']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')
    success_message = "Project '%(name)s' was created successfully."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['name', 'client', 'description', 'start_date', 'deadline', 'status']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')
    success_message = "Project '%(name)s' was updated successfully."

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Project '{obj.name}' was deleted.")
        return super().delete(request, *args, **kwargs)

# Task Views
class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'projects/task_form.html'
    success_message = "Task created successfully."

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs['project_id'], owner=self.request.user)
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_id']})

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'due_date']
    template_name = 'projects/task_form.html'
    success_message = "Task updated."

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['status']
    
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'projects/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

# Reminder Views
class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'projects/reminder_list.html'
    context_object_name = 'reminders'

    def get_queryset(self):
        return Reminder.objects.filter(project__owner=self.request.user).select_related('project')

class ReminderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reminder
    fields = ['project', 'reminder_date', 'message']
    template_name = 'projects/reminder_form.html'
    success_url = reverse_lazy('reminder_list')
    success_message = "Reminder set successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['project'].queryset = Project.objects.filter(owner=self.request.user)
        return form

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings.html'
