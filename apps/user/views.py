<<<<<<< HEAD
from pyexpat import model
from venv import create
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages




def custom_login(request):
    if request.method == 'POST':
        user = authenticate(request,
            phone_number=request.POST.get('phone_number'),
            password =request.POST.get('password')
        )
        
        if not user:
            messages.info(request , "bunday foydalanuvchi  mavjud emas")
            print(user)
            return redirect("custom_login")
        print(user)
        login(request, user)
        if user.role == 'director':
            return redirect("dashboard")
        elif user.role == 'shop':
            return redirect("shop")
    return render(request , "login.html")






=======
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def custom_login(request):
    if request.method == 'POST':
        user = authenticate(
            phone=request.POST.get("phone"),
            password=request.POST.get("password")
        )
        if not user:
            messages.info(request, "User not found")
            return redirect("custom_login")
        login(request, user)
        return redirect("dashboard")
    return render(request, 'login.html')
>>>>>>> 3e926e411d5d33307a5b53b109d2f3a29e998f45
