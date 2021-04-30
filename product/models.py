from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    STATUS = (
        ("False", "Yanlış"),
        ("True", "Doğru")
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name="İsim")
    keywords = models.CharField(
        max_length=255, verbose_name="Anahtar Kelimeler")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    image = models.ImageField(verbose_name="Resim",
                              upload_to="images", blank=True)
    status = models.CharField(verbose_name="Durum",
                              max_length=5, choices=STATUS)
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS = (
        ("False", "Yanlış"),
        ("True", "Doğru")
    )
    title = models.CharField(max_length=255, verbose_name="İsim")
    keywords = models.CharField(
        max_length=255, verbose_name="Anahtar Kelimeler")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    image = models.ImageField(verbose_name="Resim",
                              upload_to="images/", blank=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE)
    detail = RichTextField()
    price = models.FloatField()
    amount = models.IntegerField()
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True)
