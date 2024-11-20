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
    path('member_details/<int:user_acct_id>/', member_details, name='member_details'),
    path('edit-gym/<int:gym_id>/', edit_gym_content, name='edit_gym_content'),
    path('home_owner/getClass/', getClass, name='getClass'),
    path('pay_class/', pay_class, name='pay_class'),
    path('get_user_classes/', get_user_classes, name='get_user_classes'),
    path('get_instructors/', get_instructors, name='get_instructors')
   # path('delete-class/', delete_class, name='delete_class')
]