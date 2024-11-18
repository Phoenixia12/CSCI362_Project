from django.urls import path

from .views import *

#from frontend import views

#from api.views import main
from django.http import HttpResponse

def test_message(request):
    return HttpResponse("This is a test message.")


urlpatterns = [
    path('home/', home_goer, name = 'home' ),
    path('', index),
    path('login/', login_view, name='login'),  
    path('select_role/', select_role, name='select_role'),
    
    path('owner_setup/', owner_setup, name='owner_setup'),
    path('staff_setup/', staff_setup, name='staff_setup'),
    path('goer_setup/', goer_setup, name='goer_setup'),
    
    path('home_owner/', home_owner, name='home_owner'),
    path('add_member/', add_member, name='add_member'),
    path('add_employee/', add_employee, name='add_employee'),
    path('home_goer/', home_goer, name='home_goer'),
    path('home_staff/', home_staff, name='home_staff'),

    path('register/test_reg/', register_account, name='register_account'),
    path('register/', register_account, name='register'),
    
    
    
    path('logout/', index, name = 'logout'),
   
    path('get_classes/', get_classes, name='get_classes'),
    path('get_gymID/', get_gymID, name='get_gymID'),
    path('add_class/', add_class, name='add_class'),
    path('home_owner/getClass/', getClass, name='getClass'),
    path('pay_class/', pay_class, name='pay_class'),
   # path('delete-class/', delete_class, name='delete_class')
]