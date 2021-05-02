from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse


class Category(MPTTModel):
    STATUS = (
        ("False", "Yanlış"),
        ("True", "Doğru")
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name="İsim")
    keywords = models.CharField(
        max_length=255, verbose_name="Anahtar Kelimeler")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    image = models.ImageField(verbose_name="Resim",
                              upload_to="images", blank=True)
    status = models.CharField(verbose_name="Durum",
                              max_length=5, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["title"]

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return " -> ".join(full_path[::-1])

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


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
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True)
