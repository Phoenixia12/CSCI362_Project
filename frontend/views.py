from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import models


# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')


def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is found and credentials are correct, log them in
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('home')  # Redirect to the home page (or any other page)
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to the login page

    return render(request, 'login.html')

# View for register

def register_view(request):
    if request.method == "POST":
        # Getting form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if password == confirm_password:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'register.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'register.html')

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name  # Store the full name in the first_name field
            user.save()
            
            # Redirect to the login page with success message
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            # If passwords do not match
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')
    
    # If it's a GET request, just render the registration form
    return render(request, 'register.html')



def home_view(request):
    # Assume we are passing dynamic user data to the template
    user = request.user
    user_workout_data = {
        "exercises": ["Push-ups", "Pull-ups", "Squats"],
        "workout_progress": "5/7 days completed this week"
    }

    # Other data can be passed to sections like profile, contact, etc.
    context = {
        'user': user,
        'user_workout_data': user_workout_data,
        'contact_info': "Support: support@gymassist.com",
        'about_info': "GymAssist helps you track your fitness goals and progress."
    }

    return render(request, 'home.html', context)