# quizzes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz_attempt, name='submit_quiz_attempt'),
    path('quiz/<int:quiz_id>/statistics/', views.get_question_statistics, name='get_question_statistics'),
]
