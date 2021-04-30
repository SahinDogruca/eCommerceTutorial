from django.contrib import admin
from . import models
from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    try:
        list_display = ["id", "parent", "title", "update_at", "image_tag"]
    except:
        list_display = ["id", "parent", "title", "update_at"]
    list_filter = ["title", "description", "update_at"]

    def image_tag(self, obj):
        return format_html(f"<img src='{obj.image.url}' height=50 />")
    image_tag.short_description = "Image"


class ProductImageInline(admin.TabularInline):
    model = models.Image
    extra = 6


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "amount", "price", "image_tag"]
    list_filter = ["title", "description", "update_at"]
    inlines = [ProductImageInline]

    def image_tag(self, obj):
        return format_html('<img src="{}" height=50/>'.format(obj.image.url))
    image_tag.short_description = 'Image'


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "title", "image_tag"]
    list_filter = ["product", "title"]

    def image_tag(self, obj):
        return format_html(f"<img src='{obj.image.url}' height=50 />")
    image_tag.short_description = "Image"


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Image, ImageAdmin)
