from typing import Any
from django import forms
from apps.product.models import Trade
from apps.user.models import User
from apps.warehouse.models import ImportToWerhouse, Product, ProductInWarehouse, RequestToWarehouse


class AddShopWarehouseForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, required=False)
    password2 = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('name', 'address', 'phone_number', 'password1', 'password2')

    def save(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (not password1 or not password2) or (password1 != password2):
            raise forms.ValidationError("Password error")
        self.cleaned_data.pop("password2")
        self.cleaned_data['password']=self.cleaned_data.pop('password1')
        
        user = self.Meta.model.objects.create(**self.cleaned_data
        )
        user.save()
        return user
 
class ProductAddForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=("title", "description" , "category", "measure")
        
class EditshopForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('name', 'address', 'password1', 'password2', 'phone_number')
        
    def save(self, *args, **kwargs):
        password1=self.cleaned_data.pop("password1")
        password2=self.cleaned_data.pop("password2")
        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError("passwordlar xato")
        if password1 and password2:
            self.instance.set_password(password1)    
        self.instance.save()
        return self.instance
    
class EditProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=("title", "description" , "category", "measure")
        
class EditWarehouseForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('name', 'address', 'password1', 'password2', 'phone_number')
        
    def save(self, *args, **kwargs):
        password1=self.cleaned_data.pop("password1")
        password2=self.cleaned_data.pop("password2")
        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError("passwordlar xato")
        print(self.cleaned_data)
        name = self.cleaned_data.get("name")
        if name:
            self.instance.name = name
        address = self.cleaned_data.get("address")
        if address:
            self.instance.address = address
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            self.instance.phone_number = phone_number
        if password1 and password2:
            self.instance.set_password(password1)
        self.instance.save()
        return self.instance
        
        
        
class ImportProductForm(forms.ModelForm):   
    class Meta:
        model = ImportToWerhouse
        fields = ("id", 'warehouse', 'product', 'qty')
        
    def save(self, *args, **kwargs):
        product = self.cleaned_data.get("product")
        print(product)
        product_in_warehouse, _ = ProductInWarehouse.objects.get_or_create(
            warehouse_id=self.instance.warehouse.id,
            product=product
        )
        
        product_in_warehouse.qty += self.cleaned_data.get("qty")
        product_in_warehouse.save()
        self.instance.save()
        return self.instance
    
class RequestToWarehouseForm(forms.ModelForm):
    class Meta:
        model = RequestToWarehouse
        fields = ( "warehouse", "product", "qty")
        
        
class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ("id", "product", "qty")

            

    
        
