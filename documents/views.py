from typing import Any

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document
from categories.models import DocCategory
from documents.mixins import ApprovedRequiredMixin
from .forms import DocumentForm

class DocumentListView(ApprovedRequiredMixin, ListView):
    model = Document
    template_name = 'documents/doc_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.all().order_by("-timestamp")
        return context


class Dashboard(ApprovedRequiredMixin, TemplateView):
    template_name = 'documents/dashboard.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['doc_count'] = Document.objects.all().order_by("-timestamp").count()

            now = timezone.now()
            current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Calculate previous month's start date
            if current_month_start.month == 1:
                prev_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
            else:
                prev_month_start = current_month_start.replace(month=current_month_start.month - 1)

            # Counts
            current_month_count = Document.objects.filter(timestamp__gte=current_month_start).count()
            prev_month_count = Document.objects.filter(timestamp__gte=prev_month_start, timestamp__lt=current_month_start).count()

            # Difference calculation
            doc_difference = current_month_count - prev_month_count

            context['curr_month_doc_count'] = current_month_count
            context['prev_month_doc_count'] = prev_month_count
            # context['doc_difference'] = doc_difference
            context['doc_percent'] = (doc_difference/prev_month_count)*100 if prev_month_count > 0 else 0
            context['categories'] = DocCategory.objects.all()
            return context

class DocumentUploadView(ApprovedRequiredMixin, CreateView):
    model = Document
    template_name = 'documents/document_upload.html'
    success_url = '/dashboard/'
    form_class = DocumentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all()
        return context