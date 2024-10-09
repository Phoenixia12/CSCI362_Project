
#what the fucking hell. this doesnt work
from django.urls import path
from .views import main

urlpatterns = [
    path('home', main)
]