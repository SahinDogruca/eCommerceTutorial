from django.db import models
from ckeditor.fields import RichTextField


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
