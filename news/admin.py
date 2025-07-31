from django.contrib import admin
from .models import News, NewsDetail, NewsImage

class NewsDetailInline(admin.TabularInline):
    model = NewsDetail
    extra = 1

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'main_context', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('main_title', 'main_context')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [NewsDetailInline, NewsImageInline]