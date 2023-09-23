from django.urls import path
from .views import custom_login

<<<<<<< HEAD
urlpatterns = [
    path("login/" , custom_login, name="custom_login")
]
=======

urlpatterns = [
    path("login/", custom_login, name="custom_login")
]
>>>>>>> 3e926e411d5d33307a5b53b109d2f3a29e998f45
