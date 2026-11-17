from django.db import models
from categories.models import DocCategory
from django.utils import timezone


class Sender(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class DocumentType(models.TextChoices):
    INCOMING = 'IN', 'Intrare'
    OUTGOING = 'OUT', 'Ieșire'


class Compartment(models.TextChoices):
    RCEE = 'RCEE', 'Resp. Conștientizare'
    STI = 'STI', 'Specialist IT'
    BIOLOG = 'BIO', 'Biolog'
    CONTABILITATE = 'CON', 'Contabil Șef'
    DIRECTOR = 'DIR', 'Director'
    PAZA = 'PAZA', 'Pază'
    SSM = 'SSM', 'Securitate și Sănătate în Muncă'
    MECANIZARE = 'MEC', 'Mecanizare'

class Document(models.Model):
    reg_year = models.DateField()
    reg_number = models.IntegerField()
    file = models.FileField(upload_to='documents/%Y/%m/', blank=True, null=True, verbose_name="Fișier Atașat")
    timestamp = models.DateField(default=timezone.now)
    sender = models.CharField(max_length=150, unique=False, blank=True, null=True)
    sender_reg_nr = models.IntegerField(blank=True, null=True)
    sender_reg_date = models.DateField(default=None, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(DocCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="doc_category")
    doc_type = models.CharField(
        max_length=3, 
        choices=DocumentType.choices, 
        default=DocumentType.INCOMING,
        verbose_name="Tip Document"
    )
    description = models.CharField(max_length=300, unique=False, blank=True)
    responsible_compartment = models.CharField(
        max_length=30, 
        choices=Compartment.choices, 
        default=Compartment.DIRECTOR,
        verbose_name="Compartiment"
    )

    class Meta:
        ordering = ['pk']
        unique_together = ('reg_number', 'reg_year') # enforces a unique reg number per year

    def save(self, *args, **kwargs):
        if not self.pk:
            # determine the year
            year = self.timestamp if self.timestamp else timezone.now().year
            self.reg_year = year
            # get the last doc number
            last_doc = Document.objects.filter(reg_year=year).order_by("-reg_number").first()
            if last_doc and last_doc.reg_number:
                # increment the last doc nr
                self.reg_number = last_doc.reg_number + 1
            else:
                self.reg_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reg_number:04d}/{self.reg_year}"
