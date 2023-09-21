from django.contrib import admin
from .models import (
    Product,
    Category,
    Client,
    Trade,
    ShopProduct,
    ProductSellPrice
)

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'shop', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'shop')


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'sold_price', 'qty', 'created_at')


@admin.register(ProductSellPrice)
class ProductSellPriceAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', 'price')
