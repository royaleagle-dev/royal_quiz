from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_test, name = 'index_test'),
    path('quiz_page/<int:pk>', views.quiz_page, name = 'quiz_page'),
    path('<int:pk>/mark/', views.mark, name = 'mark'),
    path('signup/', views.signup, name = 'signup'),
    path('end_exam/', views.end_exam, name = 'end_exam'),
    path('<str:category>/', views.category_detail, name = 'category_detail'),

]