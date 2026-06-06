import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Pastikan tabel diagnosa_keluhan sudah ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS diagnosa_keluhan (
    id_diagnosa INTEGER PRIMARY KEY AUTOINCREMENT,
    kata_kunci TEXT NOT NULL UNIQUE,
    gejala TEXT NOT NULL,
    solusi_analisis TEXT NOT NULL
)
''')

# 2. Baca data diagnosa bawaan dari berkas JSON
JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'seeder_data', 'diagnosa_seed.json')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    diagnosa_data = json.load(f)
diagnosa_seed = [(item['kata_kunci'], item['gejala'], item['solusi_analisis']) for item in diagnosa_data]

# 3. Masukkan data ke database (gunakan INSERT OR IGNORE agar tidak duplikat)
inserted_count = 0
for kata_kunci, gejala, solusi in diagnosa_seed:
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO diagnosa_keluhan (kata_kunci, gejala, solusi_analisis) VALUES (?, ?, ?)",
            (kata_kunci, gejala, solusi)
        )
        if cursor.rowcount > 0:
            inserted_count += 1
    except sqlite3.Error as e:
        print(f"Eror saat memasukkan {kata_kunci}: {e}")

conn.commit()
conn.close()

print(f"Berhasil menginisialisasi database! Menambahkan {inserted_count} data diagnosa bawaan.")
