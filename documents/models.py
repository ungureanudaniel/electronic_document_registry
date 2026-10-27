from django.db import models
from categories.models import DocCategory, DocType
from django.utils import timezone


class Document(models.Model):
    reg_year = models.DateField()
    reg_number = models.IntegerField()
    timestamp = models.DateField()
    sender = models.CharField(max_length=150, unique=False, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(DocCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="doc_category")
    doc_type = models.ForeignKey(DocType, on_delete=models.SET_NULL, null=True, blank=True, related_name="doc_type")
    description = models.CharField(max_length=300, unique=False, blank=True)
    responsible_compartment = models.CharField(max_length=100, blank=True)

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
        return f"REG-{self.reg_year}-{self.reg_number:04d}"
