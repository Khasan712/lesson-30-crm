from django.db import models
from apps.product.enums import Measure
from apps.user.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True , blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    measure = models.CharField(max_length=20, choices=Measure.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    @property
    def price(self):
        return ProductSellPrice.objects.filter(product_id=self.id).last()

class ShopProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveBigIntegerField(default=0)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Trade(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="shop_trade")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='shop_product')
    sold_price = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

class ProductSellPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_price')
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product.title} --> {self.price}"
    