from typing import Any, Dict
from django import forms
from apps.product.models import Product, Trade
from apps.user.models import User
from django.core.exceptions import ValidationError
from apps.warehouse.models import ImportToWarehouse, ProductInWarehouse, RequestToWarehouse

class AddShopWarehouseForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('name', 'address', 'password1', 'password2', 'phone')
    
    def save(self, commit):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (not password1 or not password2) or (password1 != password2):
            raise forms.ValidationError("Password error")

        self.cleaned_data.pop("password2")
        self.cleaned_data['password'] = self.cleaned_data.pop('password1')

        user = self.Meta.model.objects.create(
            **self.cleaned_data
        )
        user.save()
        return user


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("title", 'description', 'category', 'measure')


class EditShopForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, required=False)
    password2 = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('name', 'address', 'password1', 'password2', 'phone')

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not valid:
            return valid
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (password1 and password2) and (password1 != password2):
            self.add_error("password1", ValidationError('passwords are not the same', 'passwd_mismatch'))
        if not self.errors:
            return True
        return False
    

    def save(self, *args, **kwargs):
        password1 = self.cleaned_data.pop('password1')
        password2 = self.cleaned_data.pop('password2')
        if password1 and password2:
            self.instance.set_password(password1)
        self.instance.save()
        return self.instance


class ImportProductForm(forms.ModelForm):
    class Meta:
        model = ImportToWarehouse
        fields = ("id", 'warehouse', 'product', 'qty')
    
    def save(self, *args, **kwargs):
        product = self.cleaned_data.get("product")
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
        fields = ('warehouse', 'product', 'qty')


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ('product', 'qty')