from django.urls import path
from . import views

urlpatterns = [
    path("", views.userProfile, name="user_profile"),
    path("changepassword/", views.change_password, name="change_password"),
    path('update/', views.user_update, name='user_update'),
]
