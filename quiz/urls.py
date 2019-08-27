from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('quiz_page/<str:subject>/<int:pk>/', views.quiz_page, name = 'quiz_page'),
    path('<int:pk>/mark/<str:subject>', views.mark, name = 'mark'),
    #path('signup/', views.signup, name = 'signup'),
    path('end_exam/', views.end_exam, name = 'end_exam'),
    path('<str:category>/', views.category_detail, name = 'category_detail'),
    path('set_quiz/<str:subject>/', views.quiz_param, name = 'select'),
    path('set_quiz/process/<str:subject>/', views.process, name = 'process'),
    path('quiz/postProcessor/', views.postProcessor, name = 'postProcessor'),
    

]