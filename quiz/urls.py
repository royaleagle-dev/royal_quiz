from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('mark/', views.mark, name = 'mark'),
    #path('signup/', views.signup, name = 'signup'),
    path('end_exam/', views.end_exam, name = 'end_exam'),
    path('set_quiz/', views.pre_quiz, name = 'pre_quiz'),
    #path('set_quiz/process/<str:subject>/', views.process, name = 'process'),
    path('quiz/postProcessor/', views.postProcessor, name = 'postProcessor'),
    path('quiz_page/', views.quiz_page, name = 'quiz_page'),
    path('news/', views.NewsListView.as_view(), name = 'news'),
    path('about/', views.about, name = 'about')
]