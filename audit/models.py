from django.db import models
from django.conf import settings

class DocumentAuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Înregistrare'),
        ('UPDATE', 'Modificare'),
        ('DELETE', 'Ștergere'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Utilizator"
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name="Acțiune")
    document_reg_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Număr Înregistrare")
    document_description = models.TextField(blank=True, null=True, verbose_name="Descriere Document")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data și Ora")
    details = models.TextField(blank=True, null=True, verbose_name="Detalii Suplimentare")

    class Meta:
        verbose_name = "Jurnal Audit Document"
        verbose_name_plural = "Jurnale Audit Documente"
        ordering = ['-timestamp']

    def __str__(self):
        username = self.user.username if self.user else "Sistem / Necunoscut"
        action_display = dict(self.ACTION_CHOICES).get(self.action, self.action)
        return f"[{self.timestamp.strftime('%d.%m.%Y %H:%M')}] {username} - {action_display} (Reg: {self.document_reg_number or 'N/A'})"
