from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('questions/create/', views.QuestionCreate.as_view(),
         name='questions_create'),
    path('questions/<int:question_id>/',
         views.question_detail, name='question_detail'),
]
