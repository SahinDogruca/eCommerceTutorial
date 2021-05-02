from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.contrib.auth.models import User
from django.forms import ModelForm


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def price(self):
        return (self.product.price)


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Preparing", "Preparing"),
        ("OnShipping", "OnShipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    total = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS)
    ip = models.CharField(max_length=30, blank=True)
    adminnote = models.CharField(max_length=30, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name",
                  "address", "phone", "city", "country"]


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
