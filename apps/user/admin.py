from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'first_name' , 'last_name', 'phone_number', 'created_at')
