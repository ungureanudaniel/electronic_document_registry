import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Document
from django.utils import timezone


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'doc_type', 
            'reg_number', 
            'timestamp', 
            'sender', 
            'sender_reg_nr', 
            'category',
            'description', 
            'sender_reg_date', 
            'responsible_compartment'
            ]
        widgets = {
            'file': forms.FileInput(attrs={
                'required': False,
                'class': 'absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10'
            }),
            'reg_number': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'w-full px-3.5 py-2.5 bg-slate-100 border border-slate-300 rounded-lg text-sm text-slate-500 cursor-not-allowed focus:outline-none transition',
                'placeholder': 'ex: 1234'
            }),
            'timestamp': forms.DateInput(
                            format='%Y-%m-%d',
                            attrs={
                                'type': 'date',
                                'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
                            }
                        ),
            'doc_type': forms.Select(attrs={
                            'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
                        }),
            
            'description': forms.Textarea(attrs={
                            'rows': 3,
                            'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition',
                            'placeholder': 'Scurtă descriere a conținutului documentului sau instrucțiuni de procesare...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
            }),
            'sender': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition',
                'placeholder': 'Proveniență document'
                }),
            'sender_reg_nr': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition',
                'placeholder': 'ex: 450'
            }),
            'sender_reg_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
                }
            ),
            'responsible_compartment': forms.Select(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition'
            }),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Autofill only when creating a new document
        if not self.instance.pk and not self.initial.get('reg_number'):
            today_str = timezone.now().strftime('%d.%m.%Y')
            self.initial['internal_ref_number'] = f"001/REG/{today_str}"

    def clean(self):
        cleaned_data = super().clean()
        doc_type = cleaned_data.get('doc_type')

        # if the document type is outgoing (ex. 'OUT') clear sender info automatically
        if doc_type == 'OUT':
            cleaned_data['sender'] = ''
            cleaned_data['sender_reg_nr'] = None
            cleaned_data['sender_reg_date'] = None
            
        return cleaned_data

    def clean_reference_number(self):
        ref_num = self.cleaned_data.get('reg_number')
        if not ref_num:
            raise ValidationError("Numărul de înregistrare este obligatoriu.")

        # Strip whitespace and convert to uppercase for consistency
        ref_num = ref_num.strip().upper()

        pattern = r"^[A-Z0-9\-]+/[A-Z]{3}/\d{2}\.\d{2}\.\d{4}$"

        if not re.match(pattern, ref_num):
            raise ValidationError(
                "Format invalid! Respectați structura: NumărExpeditor/INI(3 Litere de la nume și prenume)/ZZ.LL.AAAA "
                "(Exemplu: 12345/ABC/28.10.2026). Dacă nu există inițiale, nu treceți nimic."
            )

        return ref_num