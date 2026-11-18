from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from documents.mixins import ApprovedRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from django.contrib.auth import get_user_model
from documents.views import AdminStaffRequiredMixin
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.views.generic import ListView, CreateView, View
from django.utils.decorators import method_decorator
from axes.decorators import axes_dispatch
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class UserListView(ApprovedRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['active_page'] = 'user_list'
            return context



class CustomSignupView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_message = "Contul dvs. a fost creat! Vă rugăm așteptați acceptul administratorului de sistem. Veți primit un email de confirmare a contului."
    success_url = reverse_lazy('dashboard')

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


User = get_user_model()


class SecureUserRevokeView(AdminStaffRequiredMixin, View):
    template_name = 'users/user_confirm_revoke.html'

    def get(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        
        # Prevent admin from revoking themselves
        if target_user == request.user:
            messages.error(request, "Nu vă puteți revoca propriul cont de administrator.")
            return redirect('user_list')
            
        return render(request, self.template_name, {'target_user': target_user, 'active_page': 'user_list'})

    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        
        if target_user == request.user:
            messages.error(request, "Nu vă puteți revoca propriul cont de administrator.")
            return redirect('userlist')

        password = request.POST.get('admin_password')

        # Verify the logged-in admin's password
        if request.user.is_staff and request.user.check_password(password):
            target_user.is_active = False  # Deactivate / revoke user
            target_user.save()
            messages.success(request, f"Utilizatorul {target_user.email or target_user.username} a fost revocat cu succes.")
            return redirect('userlist')
        else:
            messages.error(request, "Parolă de administrator incorectă. Revocarea a eșuat.")
            return render(request, self.template_name, {
                'target_user': target_user, 
                'active_page': 'userlist'
            })


class SecureUserDeleteView(AdminStaffRequiredMixin, View):
    template_name = 'users/user_confirm_delete.html'

    def get(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        
        # Prevent admin from deleting themselves
        if target_user == request.user:
            messages.error(request, "Nu vă puteți șterge propriul cont de administrator.")
            return redirect('userlist')
            
        return render(request, self.template_name, {'target_user': target_user, 'active_page': 'user_list'})

    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        
        if target_user == request.user:
            messages.error(request, "Nu vă puteți șterge propriul cont de administrator.")
            return redirect('userlist')

        password = request.POST.get('admin_password')

        # Verify the logged-in admin's password securely
        if request.user.is_staff and request.user.check_password(password):
            username_display = target_user.email or target_user.username
            target_user.delete()
            messages.success(request, f"Utilizatorul {username_display} a fost șters definitiv.")
            return redirect('userlist')
        else:
            messages.error(request, "Parolă de administrator incorectă. Ștergerea a eșuat.")
            return render(request, self.template_name, {
                'target_user': target_user, 
                'active_page': 'userlist'
            })


@staff_member_required
def approve_user(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_approved = True
        user.save()
    return redirect('userlist')
