from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Membuat Blueprint 'auth'
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            # Ganti di sini: tambahkan kategori 'error'
            flash('Username sudah digunakan, silakan pilih yang lain.', 'error')
            return redirect(url_for('auth.signup'))
            
        new_user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        
        # Ganti di sini: tambahkan kategori 'success'
        flash('Akun berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = user.username
            return redirect(url_for('main.materi'))
            
        # Ganti di sini: tambahkan kategori 'error'
        flash("Username atau password salah!", 'error')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()  # Menghapus SEMUA data dari session
    flash('Anda telah berhasil logout.', 'success') # Tambahan: Beri pesan konfirmasi
    return redirect(url_for('auth.login'))