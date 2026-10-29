from django.db import models

class DocCategory(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Activă")


    class Meta:
        verbose_name = "Categorie Document"
        verbose_name_plural = "Categorii Documente"
        ordering = ['name']

    def __str__(self):
        return self.name


class DocType(models.Model):
    categorie = models.ForeignKey(DocCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="doc_type")
    name = models.CharField(max_length=150, unique=False, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Activă")

    class Meta:
        verbose_name = "Tip Document"
        verbose_name_plural = "Tipuri de Documente"
        ordering = ['name']
    
    def __str__(self):
            return self.name