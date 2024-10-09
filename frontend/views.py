from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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
            return redirect('index')  # Redirect to the home page (or any other page)
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to the login page

    return render(request, 'login.html')

# View for register
def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            # Simulate saving user info to the database
            return HttpResponse("Registration successful!")
        else:
            return HttpResponse("Passwords do not match!")
    return render(request, 'register.html')