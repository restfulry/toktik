from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('questions/new/', views.QuestionCreate.as_view(), name='questions_create'),
]
