from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.reports_dashboard, name='reports_dashboard'),
    path('export/csv/', views.export_projects_csv, name='export_projects_csv'),
]
