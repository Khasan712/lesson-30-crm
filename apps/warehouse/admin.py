from django.contrib import admin
from apps.warehouse.models import ImportToWarehouse, ProductInWarehouse, RequestToWarehouse


@admin.register(ImportToWarehouse)
class ImportToWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", 'warehouse', 'product', 'qty', 'created_at')


@admin.register(ProductInWarehouse)
class ProductInWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", 'warehouse', 'product', 'qty', 'created_at', 'updated_at')

@admin.register(RequestToWarehouse)
class RequestToWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'warehouse', 'product', 'qty', 'status', 'created_at', 'updated_at')

