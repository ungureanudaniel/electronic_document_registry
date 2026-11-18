from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from audit.models import DocumentAuditLog
from documents.views import AdminStaffRequiredMixin
from .models import DocCategory
from documents.mixins import ApprovedRequiredMixin
from .forms import CategoryForm

def can_approve_categories(user):
    if not user.is_authenticated:
        return False
    # Admins/Superusers or users in the accounting department
    is_admin = user.is_superuser or user.is_staff
    is_contabil_sef = getattr(user, 'compartment', None) == 'CON'
    return is_admin or is_contabil_sef


class CategoryManagementView(ApprovedRequiredMixin, CreateView):
    template_name = 'management/category_management.html'
    model = DocCategory
    form_class = CategoryForm
    success_url = reverse_lazy('category_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all().order_by('name')
        context['active_page'] = 'category_management'
        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        if self.request.user.is_superuser or getattr(self.request.user, 'compartment_code', None) == 'CON':
            category.is_active = True
        else:
            category.is_active = False
        category.save()
        
        return super().form_valid(form)


class CategoryUpdateView(ApprovedRequiredMixin, UpdateView):
    template_name = 'management/category_update.html'
    model = DocCategory
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all().order_by('name')
        context['active_page'] = 'category_management'
        return context
