from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
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


class NewCategoryView(ApprovedRequiredMixin, CreateView):
    model = DocCategory
    template_name = 'new_category.html'
    success_url = '/'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all()
        context['active_page'] = 'categories'
        context['can_approve'] = can_approve_categories(self.request.user)
        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        
        # Only Admin or Contabil Șef can instantly approve (set is_active=True)
        if can_approve_categories(self.request.user):
            category.is_active = True
            messages.success(self.request, "Categoria a fost creată și aprobată cu succes.")
        else:
            category.is_active = False
            messages.info(self.request, "Categoria a fost trimisă cu succes și așteaptă aprobarea Contabilului Șef.")
            
        category.save()
        return redirect(self.get_success_url())

class CategoryUpdateView(AdminStaffRequiredMixin, UpdateView):
    model = DocCategory
    fields = ['name', 'is_active']
    template_name = 'documents/category_form.html'
    success_url = reverse_lazy('category_management')

    def form_valid(self, form):
        messages.success(self.request, "Categoria a fost actualizată cu succes.")
        return super().form_valid(form)


class CategoryDeleteView(AdminStaffRequiredMixin, DeleteView):
    model = DocCategory
    template_name = 'documents/category_confirm_delete.html'
    success_url = reverse_lazy('category_management')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Categoria a fost ștearsă.")
        return super().delete(request, *args, **kwargs)