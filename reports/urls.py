from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('audit/', views.AuditLogListView.as_view(), name='audit_logs'),
    path('generate/', views.GenerateReportView.as_view(), name='generate_report'),
]
