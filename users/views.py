from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import CustomUser
from django.http import HttpResponse, JsonResponse
import requests


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("fullName")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        land_acres = request.POST.get("landAcres")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = CustomUser.objects.create(
            username=username,
            full_name=full_name,
            dob=dob,
            email=email,
            land_acres=land_acres,
            password=make_password(password),  # hashes password
        )
        login(request, user)
        messages.success(request, "Signup successful!")
        return redirect("dashboard")  # change to your dashboard route

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")



def logout_view(request):
    logout(request)
    return redirect('/')


def dashboard_view(request):
    return render(request, "main.html")


def fetch_news(request):
    url = "https://newsapi.org/v2/everything?q=agriculture&language=en&sortBy=publishedAt&pageSize=10&apiKey=88184fb99ec74b0aa3257dac3b83f9ff"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)
