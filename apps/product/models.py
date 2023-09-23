from operator import truediv
from turtle import mode
from django.db import models
# from apps.warehouse import product, warehouse
from apps.user.models import User


class Category(models.Model):
    title=models.CharField(max_length=100)
    # parent=models.ForeignKey( )


    def __str__(self):
        return self.title
    
    


class Product(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    measure=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,  editable=True , blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def price(self):
        return ProductSellPrice.objects.filter(product_id=self.id).last()
    

        
class ImportToShop(models.Model):
    # shop=models.ForeignKey()
    # warehouse=models.ForeignKey()
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=100)

    def __str__(self):
        return self.product


class UserRole(models.Model):
    admin=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shop=models.ForeignKey(ImportToShop, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.admin
    
class Warehouse(models.Model):
    title=models.CharField(max_length=100)
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class ProductInshop(models.Model):
    # shop=models.ForeignKey()
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.shop
    
    
    
class ShopProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveBigIntegerField(default=0)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    


    

class Trade(models.Model):
    shop=models.ForeignKey(User , on_delete=models.SET_NULL, null=True, related_name="shop_trade")
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="shop_product")
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sell_price=models.IntegerField(default=0)
    qty=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

   
    
class ImportToWarehouse(models.Model):
    # warehouse=models.ForeignKey()
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty=models.PositiveIntegerField(default=0)
    # import_price=models.ForeignKey()


    def __str__(self):
        return self.warehouse
    
class Client(models.Model):
    name=models.CharField(max_length=100)
    phone_nomer=models.TextField(max_length=100)
    # shop=models.ForeignKey()


    def __str__(self):
        return self.name
    

    def __str__(self):
        return self.warehouse
    
class ProductImage(models.Model):
    image=models.ImageField(upload_to='photos')
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.image
    

class ProductSellPrice(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_price')
    price=models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.product.title} --> {self.price}"
    
    