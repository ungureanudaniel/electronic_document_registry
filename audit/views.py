from django.shortcuts import render
from audit.models import DocumentAuditLog
from django.views.generic import ListView

from documents.views import AdminStaffRequiredMixin


class AuditLogListView(AdminStaffRequiredMixin, ListView):
    model = DocumentAuditLog
    template_name = 'audit/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'audit_logs'
        return context