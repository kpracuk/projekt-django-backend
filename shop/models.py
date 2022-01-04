from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    status = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_at_buy = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
