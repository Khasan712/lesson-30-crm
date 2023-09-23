from django.db import models

from apps.user.models import User
from apps.product.models import Product
from apps.warehouse.enum import RequestStatus


class ImportToWerhouse(models.Model):
    warehouse = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.warehouse.name} - {self.product}"

   
    
class ProductInWarehouse(models.Model):
    warehouse = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    qty=models.FloatField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.warehouse.name} - {self.product}"
    
    
class RequestToWarehouse(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , related_name='shop_request')
    warehouse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='warehouse_request')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.FloatField(default=0)
    status = models.CharField(max_length=9, choices=RequestStatus.choices(), default=RequestStatus.choices()[0][0]) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.shop.name}, {self.warehouse.name}, {self.status}"
       
    def warehouse_qty(self):
        qty = ProductInWarehouse.objects.filter(
            product_id=self.product.id, warehouse_id=self.warehouse.id
        ).first()
        
        
        return qty.qty if qty else 0   
    