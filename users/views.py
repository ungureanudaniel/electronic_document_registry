from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from axes.decorators import axes_dispatch
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

class CustomSignupView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_message = "Contul dvs. a fost creat! Vă rugăm așteptați acceptul administratorului de sistem. Veți primit un email de confirmare a contului."
    success_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('login')


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = "Bine ați venit!"
    form_class = CustomLoginForm
    # This decorator helps Axes track login attempts
    @method_decorator(axes_dispatch)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('userlist')
    
    def form_valid(self, form):
        # Axes will automatically track successful logins
        response = super().form_valid(form)
        return response


# ============== user logout view ==============
class CustomLogoutView(LogoutView):
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            
            # Instead of error, redirect to a confirmation page or home
            messages.info(request, "Vă rugăm să folosiți butonul de logout pentru a vă deconecta.")
            return redirect('dashboard')
            
        messages.success(request, "Ați fost deconectat cu succes.")
        return super().dispatch(request, *args, **kwargs)

@staff_member_required
def approve_user(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_approved = True
        user.save()
    return redirect('userlist')

@staff_member_required
def revoke_user(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_approved = False
        user.save()
    return redirect('userlist')

@staff_member_required
def delete_user(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
    return redirect('userlist')