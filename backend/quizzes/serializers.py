# quizzes/serializers.py

from rest_framework import serializers
from .models import User, Quiz, Question, Option, OptionStats

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        return user


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'pass_mark', 'question_count', 'unique_link']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'user_name', 'score', 'passed', 'completed_at']


class OptionStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionStats
        fields = ['click_count']
