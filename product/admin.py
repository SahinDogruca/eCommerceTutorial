from django.contrib import admin
from . import models
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Category


class ProductImageInline(admin.TabularInline):
    model = models.Image
    extra = 6


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "amount", "price", "image_tag"]
    list_filter = ["title", "description", "update_at"]
    prepopulated_fields = {'slug': ('title',)}
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


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        # ! it is not an error
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        # ! it is not an error
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Image, ImageAdmin)
