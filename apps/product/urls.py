from django.urls import path
from .views import Shop

urlpatterns = [
     path("", Shop.as_view(), name='shop'),
]
