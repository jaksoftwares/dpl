from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from projects.models import Project, Task
from django.db.models import Count, Q, Avg, F
import csv
import json
from django.utils import timezone
from datetime import timedelta

@login_required
def reports_dashboard(request):
    user = request.user
    projects = Project.objects.filter(owner=user)
    completed_projects = projects.filter(status='COMPLETED')
    
    # Performance Metrics
    total_completed = completed_projects.count()
    on_time_count = 0
    overdue_count = 0
    
    project_durations = []
    
    for p in completed_projects:
        if p.completed_at and p.deadline:
            if p.completed_at.date() <= p.deadline:
                on_time_count += 1
            else:
                overdue_count += 1
        
        if p.completed_at and p.start_date:
            duration = (p.completed_at.date() - p.start_date).days
            project_durations.append(duration)

    avg_duration = sum(project_durations) / len(project_durations) if project_durations else 0

    # Data for Charts
    # 1. Status Distribution
    status_data = list(projects.values('status').annotate(count=Count('id')))
    status_labels = [s['status'] for s in status_data]
    status_values = [s['count'] for s in status_data]

    # 2. Monthly Completion Trends (Last 6 months)
    today = timezone.now().date()
    months = []
    completion_trends = []
    for i in range(5, -1, -1):
        first_day_of_month = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month = (first_day_of_month + timedelta(days=32)).replace(day=1)
        count = completed_projects.filter(completed_at__range=[first_day_of_month, next_month]).count()
        months.append(first_day_of_month.strftime('%b %Y'))
        completion_trends.append(count)

    context = {
        'total_projects': projects.count(),
        'completed_count': total_completed,
        'on_time_count': on_time_count,
        'overdue_count': overdue_count,
        'avg_duration': round(avg_duration, 1),
        'completed_projects': completed_projects.order_by('-completed_at')[:10],
        
        # Chart JSON data
        'status_labels_json': json.dumps(status_labels),
        'status_values_json': json.dumps(status_values),
        'trend_labels_json': json.dumps(months),
        'trend_values_json': json.dumps(completion_trends),
        'performance_data_json': json.dumps([on_time_count, overdue_count]),
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def export_projects_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="completed_projects_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Project Name', 'Client', 'Start Date', 'Deadline', 'Completed At', 'Status', 'Progress'])

    projects = Project.objects.filter(owner=request.user, status='COMPLETED').order_by('-completed_at')
    for p in projects:
        writer.writerow([
            p.name, 
            p.client or 'N/A', 
            p.start_date, 
            p.deadline, 
            p.completed_at.strftime('%Y-%m-%d %H:%M') if p.completed_at else 'N/A',
            p.status, 
            f"{p.progress}%"
        ])

    return response
