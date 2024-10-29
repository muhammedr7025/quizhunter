# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    quizzes = db.relationship('Quiz', backref='author', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempts = db.Column(db.Integer, default=0)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')
    correct_answer = db.Column(db.Integer, nullable=False)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({
            'user_id': user.id,
            'username': user.username
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    user_id = data['user_id']  # In production, get this from session/token
    
    quiz = Quiz(
        title=data['title'],
        user_id=user_id
    )
    db.session.add(quiz)
    db.session.flush()
    
    for q_data in data['questions']:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data['question'],
            correct_answer=q_data['correctAnswer']
        )
        db.session.add(question)
        db.session.flush()
        
        for opt_text in q_data['options']:
            option = Option(
                question_id=question.id,
                option_text=opt_text
            )
            db.session.add(option)
    
    db.session.commit()
    return jsonify({'quiz_id': quiz.id}), 201

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = []
    
    for question in quiz.questions:
        options = [option.option_text for option in question.options]
        questions.append({
            'id': question.id,
            'question': question.question_text,
            'options': options,
            'correctAnswer': question.correct_answer
        })
    
    # Randomize question order for participants
    random.shuffle(questions)
    
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'questions': questions,
        'attempts': quiz.attempts
    })

@app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz_attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    # Increment attempts counter
    quiz.attempts += 1
    db.session.commit()
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz.questions)
    
    for answer in data['answers']:
        question = Question.query.get(answer['question_id'])
        if question.correct_answer == answer['selected_option']:
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    
    return jsonify({
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': total_questions
    })

@app.route('/api/users/<int:user_id>/quizzes', methods=['GET'])
def get_user_quizzes(user_id):
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': quiz.id,
        'title': quiz.title,
        'attempts': quiz.attempts,
        'created_at': quiz.created_at.isoformat()
    } for quiz in quizzes])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)