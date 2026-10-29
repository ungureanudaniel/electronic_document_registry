import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['reg_number', 'sender', 'doc_type']

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