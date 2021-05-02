from django.contrib import admin
from .models import *


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "subject", "status"]
    list_display_links = ["id", "name", "email", "subject", "status"]
    list_filter = ["name", "email", "subject", "status"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "user", "product", "status"]
    list_display_links = ["id", "subject", "user", "product", "status"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user_name", "phone",
                    "address", "city", "country", "image_tag"]
    list_display_links = ["user_name", "phone",
                          "address", "city", "country", "image_tag"]


admin.site.register(Setting)
admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
