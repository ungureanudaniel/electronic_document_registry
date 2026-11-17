from typing import Any
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import DeleteView, ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Document
from categories.models import DocCategory
from django.contrib import messages
from documents.mixins import ApprovedRequiredMixin
from .forms import DocumentForm
from django.contrib.auth import authenticate

def get_user_initials(user):
    """
    Extracts uppercase initials from user's full name.
    """
    full_name = f"{user.last_name} {user.first_name}".strip()
    if not full_name and hasattr(user, "get_full_name"):
        full_name = user.get_full_name()
    elif not full_name:
        full_name = 'DIR'

    words = full_name.split()
    initials = "".join(word[0].upper() for word in words)
    return initials


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        request = getattr(self, "request", None)
        user = getattr(request, "user", None) if request else None
        return bool(
            getattr(user, "is_authenticated", False)
            and getattr(user, "is_staff", False)
        )

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
    success_url = '/'
    form_class = DocumentForm

    def form_valid(self, form):
        print("Formularul este valid! Se salvează documentul...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Câmpuri completate incorect sau lipsă:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.filter(is_active=True).order_by('name')
        return context

    def get_initial(self):
        initial = super().get_initial()
        next_nr = Document.objects.all().count() + 1
        today_str = timezone.now().strftime("%Y-%m-%d")
        initial['reg_number'] = next_nr
        initial['timestamp'] = today_str
        return initial


class CategoryManagementView(ApprovedRequiredMixin, TemplateView):
    template_name = 'management/category_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all().order_by('name')
        return context


class DocumentManagementView(ApprovedRequiredMixin, ListView):
    template_name = 'management/documents_management.html'

    def get_queryset(self):
        return Document.objects.all().order_by("-timestamp")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = self.get_queryset()
        return context


class SecureDocumentDeleteView(AdminStaffRequiredMixin, DeleteView):
    template_name = 'management/document_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_id = self.kwargs.get('pk')
        context['document'] = Document.objects.get(pk=document_id)
        return context


class OutgoingLetterCreateView(CreateView):
    model = Document
    fields = ['sender', 'description']
    template_name = 'documents/outgoing_letter_form.html'

    def form_valid(self, form):
        user = self.request.user
        initials = get_user_initials(user)
        
        # Calculate next registration sequence number (e.g., 104)
        next_seq = Document.objects.filter(doc_type='OUT').count() + 1
        today_str = timezone.now().strftime('%d.%m.%Y')
        
        # Format: 104 / NIC / 30.10.2026
        form.instance.internal_ref_number = f"{next_seq} / {initials} / {today_str}"
        form.instance.doc_type = 'OUT'
        form.instance.created_by = user
        
        return super().form_valid(form)