from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class News(models.Model):
    main_title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, default="", blank=True)
    main_context = RichTextField()
    main_image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.main_title

    class Meta:
        ordering = ['-created_at']

class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/additional/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Bu görsel için isteğe bağlı başlık")

    def __str__(self):
        return f"{self.news.main_title} - Image {self.id}"
