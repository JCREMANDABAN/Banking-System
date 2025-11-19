from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'reports/audit_logs.html'
    context_object_name = 'logs'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset().select_related('actor')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(action__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Audit Logs'
        ctx['query'] = self.request.GET.get('q', '')
        return ctx

class GenerateReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/generate_report.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Generate Report'
        ctx['summary'] = {
            'accounts': self.request.user.accounts.count(),
            'loans': self.request.user.loans.count(),
            'transactions': sum(a.transactions.count() for a in self.request.user.accounts.all()),
        }
        return ctx
