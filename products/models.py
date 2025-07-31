from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import re

# Create your models here.

class Product(models.Model):
    main_title = models.CharField(max_length=200, default="")
    sub_title = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    main_context = RichTextField(default="")
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Türkçe karakterleri İngilizce'ye çevir
            title_for_slug = self.main_title.lower()
            turkish_chars = {
                'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                'Ç': 'c', 'Ğ': 'g', 'I': 'i', 'İ': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u'
            }
            for turkish, english in turkish_chars.items():
                title_for_slug = title_for_slug.replace(turkish, english)
            
            # Slug oluştur
            base_slug = slugify(title_for_slug)
            slug = base_slug
            counter = 1
            
            # Aynı slug varsa sayı ekle
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.main_title

    class Meta:
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/additional/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.main_title} - Image {self.id}"
