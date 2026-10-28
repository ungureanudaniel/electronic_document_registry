from typing import Any

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document
from categories.models import DocCategory
from documents.mixins import ApprovedRequiredMixin


class DocumentListView(ApprovedRequiredMixin, ListView):
    model = Document
    template_name = 'documents/doc_list.html'

class Dashboard(ApprovedRequiredMixin, TemplateView):
    template_name = 'documents/dashboard.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['categories'] = DocCategory.objects.all()
            return context

class DocumentUploadView(ApprovedRequiredMixin, CreateView):
    model = Document
    fields = ['timestamp', 'category', 'sender', 'job_title', 'description', ]
    template_name = 'documents/document_upload.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all()
        return context