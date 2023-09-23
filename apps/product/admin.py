from django.contrib import admin
from .models import ( 
                    Category,
                    Product,
                    ImportToShop, 
                    UserRole,
                    Warehouse,
                    ProductInshop, 
                    # ProductInWarehouse,
                    Trade,
                    Client,
                    ProductImage,
                    ShopProduct,
                    # SellPrice
                               ) 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    
@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "product", "category", "sell_price", "qty", "created_at")
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description','category', 'measure')
    
@admin.register(ImportToShop)
class ImportToShop(admin.ModelAdmin):
    list_display = ("id","product","qty", "status")

@admin.register(UserRole)
class UserRole(admin.ModelAdmin):
    list_display = ("id", 'admin', "shop")
    
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id",'title', "address")
    
@admin.register(ProductInshop)
class ProductInshopAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "qty")
    
    
@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "shop", "qty")    
    
# @admin.register(ProductInWarehouse)
# class ProductInWarehouseAdmin(admin.ModelAdmin):
#     list_display = ("id", 'product')