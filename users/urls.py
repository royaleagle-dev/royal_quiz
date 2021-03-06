from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.signup, name = 'signup'),
    path('corelogin/', views.coreLogin, name = 'coreLogin'),
    path('dashboard/<str:username>/', views.dashboard, name = 'dashboard'),
    path('<str:username>/addquestion/', views.addQuestion, name = 'addQuestion'),
    path('dashboard/users/', views.dashboardUsers.as_view(), name = 'dashboardUsers'),
    path('dashboard/quiz/', views.dashboardQuiz, name = 'dashboardQuiz'),
    path('dashboard/profile/<str:username>/', views.profile, name = 'profile'),
    path('dashboard/profile/<str:username>/update/', views.profileUpdate, name = 'profileUpdate'),
    #path('dashboard/profileM/<str:username>/', views.profileMini, name = 'profileMini'),
    path('dashboard/scoreBoard/', views.scoreBoard.as_view(), name = 'scoreBoard'),
    path('dashboard/addQuestion/', views.addQuestion, name = 'addQuestion'),
    path('dashboard/pendingQuestions/<str:username>/', views.pendingQuestion, name = 'pendingQuestion'),
    path('dashboard/decline/<int:pk>/', views.decline, name = 'decline'),
    path('dashboard/approve/<int:pk>/', views.approve, name = 'approve'),
]