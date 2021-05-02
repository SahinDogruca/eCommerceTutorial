from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="order_index"),
    path("addtobasket/<int:id>", views.addtobasket, name="addtobasket"),
    path("deletetobasket/<int:id>", views.deletetobasket, name="deletetobasket"),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('user_orders', views.user_orders, name="user_orders"),
    path('user_order_details/<int:id>', views.user_orders_details,
         name="user_order_details"),
]
