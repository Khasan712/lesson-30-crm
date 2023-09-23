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






