from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password and confirm password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        # Username length check
        if len(username) > 10:
            messages.error(request, "Username is too long")
            return redirect('signup')

        # Password length check
        if len(password) < 3:
            messages.error(request, "Password is too short")
            return redirect('signup')

        # Create the user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()

        messages.success(request, "Your account has been created successfully")
        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')
