import re
from django import forms
from django.core.exceptions import ValidationError
from .models import DocCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = DocCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm px-3.5 py-2.5 text-slate-900 border placeholder-slate-400',
                'placeholder': 'Introduceți denumirea categoriei...'
            }),}
