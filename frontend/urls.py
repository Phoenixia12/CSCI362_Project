from django.urls import path
from .views import index
from .views import login_view
from .views import register_view
from .views import home_view

#from frontend import views

#from api.views import main
from django.http import HttpResponse

def test_message(request):
    return HttpResponse("This is a test message.")


urlpatterns = [
    path('home/', home_view, name = 'home' ),
    path('', index),
    path('login/', login_view, name='login'),  
    path('register/', register_view, name='register'), 
    path('logout/', index, name = 'logout'),
]