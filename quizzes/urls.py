from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='list'),
    path('<int:pk>/', views.quiz_detail, name='detail'),
    path('<int:pk>/submit/', views.quiz_submit, name='submit'),
    path('<int:pk>/results/', views.quiz_results, name='results'),
    path('create/', views.quiz_create, name='create'),
    path('<int:pk>/edit/', views.quiz_edit, name='edit'),
    path('<int:pk>/delete/', views.quiz_delete, name='delete'),
]
