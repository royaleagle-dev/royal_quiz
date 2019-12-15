from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.signup, name = 'signup'),
    path('corelogin/', views.coreLogin, name = 'coreLogin'),
    path('coreloginProcessor/', views.coreLoginProcessor, name = 'coreLoginProcessor'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('dashboard/users/', views.dashboardUsers.as_view(), name = 'dashboardUsers'),
    path('dashboard/quiz/', views.dashboardQuiz, name = 'dashboardQuiz'),
    path('dashboard/profile/<str:username>/', views.profile, name = 'profile'),
    path('dashboard/profile/<str:username>/update/', views.profileUpdate, name = 'profileUpdate'),
    path('dashboard/profileM/<str:username>/', views.profileMini, name = 'profileMini'),
    path('dashboard/scoreBoard/', views.scoreBoard.as_view(), name = 'scoreBoard'),
    path('dashboard/addQuestion/', views.addQuestion, name = 'addQuestion'),
    path('dashboard/approveQuestion/', views.approveQuestion, name = 'approveQuestion'),
    path('dashboard/decline/<int:pk>/', views.decline, name = 'decline'),
    path('dashboard/approve/<int:pk>/', views.approve, name = 'approve'),
]