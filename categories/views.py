from django.shortcuts import render
from .models import DocCategory
from documents.mixins import ApprovedRequiredMixin
from django.views.generic import ListView, CreateView


class NewCategoryView(ApprovedRequiredMixin, CreateView):
    model = DocCategory
    fields = ['name']
    template_name = 'documents/document_upload.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocCategory.objects.all()
        return context
