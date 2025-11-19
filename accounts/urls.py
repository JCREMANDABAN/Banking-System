from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('loan/apply/', views.loan_application_view, name='loan_apply'),
    path('loan/approve/<int:app_id>/', views.loan_approval_view, name='loan_approve'),
    path('loan/disbursement/<int:loan_id>/', views.disbursement_view, name='disbursement'),
    path('loan/repayment/<int:loan_id>/', views.repayment_view, name='repayment'),
    path('savings/', views.savings_view, name='savings'),
    path('reports/', views.reports_view, name='reports'),
    path('audit/', views.audit_logs_view, name='audit'),
]