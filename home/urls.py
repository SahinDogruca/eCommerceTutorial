from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    path('references', views.references, name="references"),
    path('contact', views.contact, name="contact"),
    path('category/<int:id>/<str:slug>',
         views.category_products, name="category_products"),
    path('product/<int:id>/<str:slug>',
         views.product_detail, name="product_detail"),
    path('addcomment/<int:id>', views.add_comment, name="add_comment"),
    path('search/', views.search, name="search"),
    path('search_auto/', views.product_auto_search, name="auto_search"),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
]
