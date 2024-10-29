# quizzes/models.py

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    pass_mark = models.IntegerField()
    unique_link = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question_count = models.IntegerField(default=10)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class OptionStats(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='stats')
    click_count = models.IntegerField(default=0)
