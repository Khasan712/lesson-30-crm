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
        if user.role == "director":
            return redirect("dashboard")
        elif user.role == 'shop':
            return redirect("shop")
    return render(request, 'login.html')
