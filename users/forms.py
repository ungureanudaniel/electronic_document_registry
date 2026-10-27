from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import CustomUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from typing import cast

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Nume utilizator sau email'),
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
            'placeholder': _('Introduceți numele sau emailul'),
            'autofocus': True
        })
    )
    # Password field with Bootstrap styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Initialize the parent class
        self.fields['password'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}) # Add Bootstrap class to password field


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label="Nume de utilizator",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
            'placeholder': _('Introduceți un nume de utilizator'),
            'autofocus': True
        }
        )
    )
    firstname = forms.CharField(
        required=True,
        label="Prenume",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
            'placeholder': _('Introduceți prenumele'),
            'autofocus': True
            }
        )
    )
    lastname = forms.CharField(
            required=True,
            label="Nume de familie",
            widget=forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
                'placeholder': _('Introduceți numele de familie'),
                'autofocus': True
                }
            )
        )
    jobtitle = forms.CharField(
            required=True,
            label="Funcție în instituție",
            widget=forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
                'placeholder': _('Introduceți funcția din instituție'),
                'autofocus': True
            }
        )
    )
    email = forms.EmailField(
        required=True, 
        label="Adresă de email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
            'placeholder': _('Introduceți emailul'),
            'autofocus': True
            })
        )
    password1 = forms.CharField(
        required=True, 
        label="Parolă",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
            'placeholder': _('Introduceți o parolă'),
            'autofocus': True
            })
        )
    password2 = forms.CharField(
            required=True, 
            label="Verificare parolă",
            widget=forms.PasswordInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm',
                'placeholder': _('Introduceți aceeași parolă'),
                'autofocus': True
                })
            )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True  # User can login
        user.is_approved = False  # needs admin approval
        if commit:
            user.save()
            user.assign_initial_group()  # Your custom method
            self.send_admin_notification(user)
        return user

    def send_admin_notification(self, user):
        """Send email to admin about new user registration"""
        subject = f'Înregistrare utilizator nou: {user.username}'
        
        # Email content for admin
        message = render_to_string('emails/admin_notification.txt', {
            'user': user,
            'admin_url': settings.ADMIN_URL,
        })
        
        admin_emails = ['danielungureanu531@gmail.com']
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            fail_silently=False,
        )

# ==============user update form=============
class UsernameEmailChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes and custom styles to form fields
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': _('Enter first name'),
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': _('Enter last name'),
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control d-flex w-100 p-2 bd-highlight',
            'placeholder': _('Enter email'),
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_approved = False  # Set new user as unapproved by default
        if commit:
            user.save()
            user.assign_initial_group()
        return user


# ==============profile edit form=============
class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'job_title', 'avatar']

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)  # Define bio with Textarea widget

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['avatar'].initial = user.avatar
            self.fields['job_title'].initial = user.job_title

        # Apply Bootstrap classes and custom styles to form fields
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter first name'),
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter last name'),
        })
        self.fields['job_title'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter job title'),
        })
        
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Attach picture of you'),
        })

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
        return user_profile


class ManagerUserForm(forms.ModelForm):
    """Form for managers to edit users (limited fields)"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Managers can only assign REPORTER or MANAGER roles
        role_field = cast(forms.ChoiceField, self.fields['role'])
        role_field.choices = [
            choice for choice in CustomUser.Role.choices 
            if choice[0] in ['REPORTER', 'MANAGER']
        ]
        # Apply Bootstrap classes and custom styles to form fields
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter first name'),
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter last name'),
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control d-flex w-100 p-2 bd-highlight',
            'placeholder': _('...'),
        })


class AdminUserForm(forms.ModelForm):
    """Form for admins to edit users (all fields)"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'role', 'is_active', 'is_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')

        if instance:
            print(f"Editing user: {instance.username}")

        # Managers can only assign REPORTER or MANAGER roles
        role_field = cast(forms.ChoiceField, self.fields['role'])
        role_field.choices = [
            choice for choice in CustomUser.Role.choices 
            if choice[0] in ['REPORTER', 'MANAGER']
        ]
        # Apply Bootstrap classes and custom styles to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('User name'),
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter first name'),
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control d-flex p-2 bd-highlight',
            'placeholder': _('Enter last name'),
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control d-flex w-100 p-2 bd-highlight',
            'placeholder': _('...'),
        })

UserManagementForm = AdminUserForm