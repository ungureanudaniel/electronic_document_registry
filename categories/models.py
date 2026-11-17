from django.db import models
from django.utils.text import slugify


class DocCategory(models.Model):
    name = models.CharField(max_length=50, unique=False, blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Activă")
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Categorie Document"
        verbose_name_plural = "Categorii Documente"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.slug

