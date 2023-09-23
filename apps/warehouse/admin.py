from django.contrib import admin
from .models import ProductInWarehouse, ImportToWerhouse, RequestToWarehouse


@admin.register(ProductInWarehouse)
class ProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "warehouse", "product","qty")


@admin.register(ImportToWerhouse)
class ImportToWerhouseAdmin(admin.ModelAdmin):
    list_display = ("id", "warehouse", "product","qty")


@admin.register(RequestToWarehouse)
class RequestToWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "shop", "warehouse", "product","qty", "status")
