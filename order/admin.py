from django.contrib import admin
from .models import Basket
from .models import OrderProduct, Order


class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]
    list_display_links = ["id", "user", "product", "quantity"]
    search_fields = ["user", "product"]


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'phone', 'city', 'total', 'status']
    list_filter = ['status']
    readonly_fields = ('user', 'address', 'city', 'country', 'phone',
                       'first_name', 'ip', 'last_name', 'phone', 'city', 'total')
    can_delete = False
    inlines = [OrderProductline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
