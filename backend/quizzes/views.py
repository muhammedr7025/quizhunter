# quizzes/views.py

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Quiz, Question, Option, OptionStats
from .serializers import UserSerializer, QuizSerializer

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists. Please choose another one.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username)
    user.set_password(password)
    user.save()
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            request.session['user_id'] = user.id
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Username does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    request.session.flush()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_quiz(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({'error': 'User not logged in.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, id=user_id)
        serializer.save(creator=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_name = request.data.get("user_name")
    answers = request.data.get("answers", [])

    score = 0
    for answer in answers:
        question = get_object_or_404(Question, id=answer['question_id'])
        correct_options = Option.objects.filter(question=question, is_correct=True)
        selected_options = Option.objects.filter(id__in=answer['selected_option_ids'])

        # Update statistics for selected options
        for selected_option in selected_options:
            option_stat, created = OptionStats.objects.get_or_create(option=selected_option)
            option_stat.click_count += 1
            option_stat.save()

        # Calculate score
        if set(correct_options) == set(selected_options):
            score += 1

    passed = score >= quiz.pass_mark
    return Response({'message': 'Quiz submitted successfully.', 'score': score, 'passed': passed}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_question_statistics(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    stats = []
    for question in questions:
        question_stats = {
            'question_id': question.id,
            'question_text': question.question_text,
            'options': []
        }
        options = Option.objects.filter(question=question)
        for option in options:
            option_stat = OptionStats.objects.filter(option=option).first()
            question_stats['options'].append({
                'option_id': option.id,
                'option_text': option.option_text,
                'click_count': option_stat.click_count if option_stat else 0
            })
        stats.append(question_stats)

    return Response(stats, status=status.HTTP_200_OK)
