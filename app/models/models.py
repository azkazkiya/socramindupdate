# app/models/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# --- [MODEL DATABASE] ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    answers = db.relationship('Answer', backref='user', lazy=True)

    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_name = db.Column(db.String(100), nullable=False)
    max_step_achieved = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Progress User {self.user_id} in {self.module_name}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    module_name = db.Column(db.String(100), nullable=False)
    step_index = db.Column(db.Integer, nullable=False)
    stage_index = db.Column(db.Integer, nullable=True) # Untuk melacak sub-langkah
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Answer {self.id} by User {self.user_id}>'

# class QuizResult(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     score = db.Column(db.Integer, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     module_name = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f'<QuizResult {self.id} by User {self.user_id}>'

class QuizAttempt(db.Model):
    """Mencatat setiap kali seorang user menyelesaikan kuis."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relasi ke setiap jawaban dalam attempt ini
    answers = db.relationship('QuizAnswer', backref='attempt', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<QuizAttempt {self.id} on {self.module_name}>'

class QuizAnswer(db.Model):
    """Menyimpan detail setiap jawaban dalam sebuah QuizAttempt."""
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    selected_answer = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<QuizAnswer {self.id} for Attempt {self.attempt_id}>'