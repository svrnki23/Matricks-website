from django.contrib import admin
from django.urls import path, include
from . import views, StudentView
#from . import StaffView

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.home, name = 'home'),
    path('contact',views.contact, name='contact'),
    path('login_page',views.loginUser,name='login'),
    path('logout_user',views.logout, name='logout'),
    path('registration_page',views.register,name='register'),
    path('login', views.dologin, name='doLogin'),
    path('regsiter',views.doRegister, name='doRegister'),
    
    #URLs for the student view
    
    
    
    #URLs for the tutor view
    
    
]
