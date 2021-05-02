from django.db.models.fields.related import OneToOneField
from product.models import Product
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.html import format_html


class Setting(models.Model):
    STATUS = (
        ("False", "Yanlış"),
        ("True", "Doğru")
    )
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    smtpserver = models.CharField(max_length=255, blank=True)
    smtpemail = models.CharField(max_length=255, blank=True)
    smtppassword = models.CharField(max_length=255, blank=True)
    smtpport = models.CharField(max_length=255, blank=True)
    icon = models.ImageField(upload_to="images/", blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    aboutus = RichTextField()
    references = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    contact = RichTextField()

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ("New", "New"),
        ("Read", "Read"),
        ("Closed", "Closed"),
    )
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    ip = models.CharField(blank=True, max_length=50)
    note = models.CharField(blank=True, max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    STATUS = (
        ("New", "New"),
        ("True", "Evet"),
        ("False", "Hayır"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.CharField(max_length=50)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    ip = models.CharField(blank=True, max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to="images/user")
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.user.username

    def user_name(self):
        return f"{self.user.first_name} {self.user.last_name} [{self.user.username}]"

    def image_tag(self):
        return format_html("<img src={} height='50' />".format(self.image.url))
