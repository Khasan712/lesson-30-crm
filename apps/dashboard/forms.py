from typing import Any
from django import forms
from apps.user.models import User


class AddShopForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255)
    password2 = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('name', 'address', 'password1', 'password2', 'phone')
    
    def save(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (not password1 or not password2) or (password1 != password2):
            raise forms.ValidationError("Password error")
        name = self.cleaned_data.get("name")
        address = self.cleaned_data.get("address")
        phone = self.cleaned_data.get("phone")

        user = self.Meta.model.objects.create_user(
            name=name,
            address=address,
            role='shop',
            phone=phone,
            password=password1
        )
        user.save()
    