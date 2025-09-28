# create_db.py

# Impor 'app' dari run.py dan 'db' dari app
from run import app
from app import db

# Gunakan 'app_context' agar skrip tahu database mana yang harus dibuat
with app.app_context():
    print("Membuat semua tabel database...")
    db.create_all()
    print("Database dan semua tabel berhasil dibuat!")