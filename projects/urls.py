from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Tasks
    path('projects/<int:project_id>/tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/status-update/', views.TaskStatusUpdateView.as_view(), name='task_status_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Reminders
    path('reminders/', views.ReminderListView.as_view(), name='reminder_list'),
    path('reminders/create/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]