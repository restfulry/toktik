from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:member_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/update/',
         views.ProfileUpdate.as_view(), name='profile_update'),
    path('questions/create/', views.QuestionCreate.as_view(),
         name='questions_create'),
    path('questions/<int:question_id>/',
         views.question_detail, name='question_detail'),
    path('questions/<int:question_id>/add_answer/',
         views.add_answer, name='add_answer'),
    path('questions/<int:pk>/update/',
         views.QuestionUpdate.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/',
         views.QuestionDelete.as_view(), name='question_delete'),
]
