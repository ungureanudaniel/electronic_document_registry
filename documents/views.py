from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Document
@login_required
def document_list(request):
    return render(request, 'documents/doc_list.html')

@login_required
def dashboard(request):
    return render(request, 'documents/dashboard.html')

class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['timestamp', 'category', 'sender', 'job_title', 'description', ]
    template_name = 'documents/document_upload.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)