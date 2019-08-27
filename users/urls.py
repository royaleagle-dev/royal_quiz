from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.signup, name = 'signup'),
    path('signup_processor/', views.signup_processor, name = 'signup_processor'),
    path('corelogin/', views.coreLogin, name = 'coreLogin'),
    path('coreloginProcessor/', views.coreLoginProcessor, name = 'coreLoginProcessor'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('dashboard/users/', views.dashboardUsers, name = 'dashboardUsers'),
]