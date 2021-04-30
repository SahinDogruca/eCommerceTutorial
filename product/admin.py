from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "parent", "title", "update_at"]
    list_filter = ["title", "description", "update_at"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "amount", "price"]
    list_filter = ["title", "description", "update_at"]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
