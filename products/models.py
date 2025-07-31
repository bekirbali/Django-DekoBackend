from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Product(models.Model):
    main_title = models.CharField(max_length=200, default="")
    sub_title = models.CharField(max_length=200, default="")
    main_context = RichTextField(default="")
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.main_title

    class Meta:
        ordering = ['-created_at']

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    context = RichTextField(blank=True)

    def __str__(self):
        return f"{self.product.main_title} - {self.title}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/additional/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.main_title} - Image {self.id}"
