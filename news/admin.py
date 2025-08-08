from django.contrib import admin
from django.utils.html import strip_tags
from .models import News, NewsImage

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image', 'title')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'cleaned_main_context', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('main_title', 'main_context')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [NewsImageInline]

    def cleaned_main_context(self, obj):
        text = strip_tags(obj.main_context)
        return (text[:150] + '...') if len(text) > 150 else text
    cleaned_main_context.short_description = 'Main Context'

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'image', 'get_title_preview')
    search_fields = ('news__main_title', 'title')
    fields = ('news', 'image', 'title')
    
    def get_title_preview(self, obj):
        if obj.title:
            return (obj.title[:30] + '...') if len(obj.title) > 30 else obj.title
        return '-'
    get_title_preview.short_description = 'Başlık Önizleme'