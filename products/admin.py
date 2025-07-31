from django.contrib import admin
from django.utils.html import strip_tags
from .models import Product, ProductDetail, ProductImage

class ProductDetailInline(admin.TabularInline):
    model = ProductDetail
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'cleaned_main_context', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('main_title', 'main_context')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductDetailInline, ProductImageInline]

    def cleaned_main_context(self, obj):
        text = strip_tags(obj.main_context)
        return (text[:150] + '...') if len(text) > 150 else text
    cleaned_main_context.short_description = 'Main Context'

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'cleaned_context')
    search_fields = ('title', 'context', 'product__main_title')

    def cleaned_context(self, obj):
        text = strip_tags(obj.context)
        return (text[:150] + '...') if len(text) > 150 else text
    cleaned_context.short_description = 'Context'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__main_title',)
