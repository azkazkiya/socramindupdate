from flask import Blueprint, render_template, session, redirect, url_for
from ..models.models import User, QuizAttempt

# Membuat Blueprint 'main'
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/materi')
def materi():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('materi.html')

@main.route('/pencapaian')
def pencapaian():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['username']).first()
    
    # Ganti query dari QuizResult menjadi QuizAttempt
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user.id).order_by(QuizAttempt.timestamp.desc()).all()

    # Kirim data 'quiz_attempts' ke template
    return render_template('pencapaian.html', quiz_history=quiz_attempts)

# --- [TAMBAHKAN BLOK KODE INI] ---
# Rute baru untuk menyajikan file HTML statis dari folder materi
@main.route('/templates/materi/<path:filename>')
def serve_materi_file(filename):
    return render_template(f'materi/{filename}')