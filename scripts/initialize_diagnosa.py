import sqlite3
import os

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

# 2. Data diagnosa bawaan (sebelumnya hardcoded di Python)
diagnosa_seed = [
    (
        'brebet gas', 
        'Motor brebet saat digas', 
        'Motor brebet saat digas biasanya disebabkan karburator atau injektor kotor.'
    ),
    (
        'brebet tanjakan', 
        'Motor brebet saat tanjakan', 
        'Motor brebet saat tanjakan biasanya karena suplai bahan bakar kurang optimal atau CVT mulai lemah.'
    ),
    (
        'brebet dingin', 
        'Motor brebet saat kondisi dingin', 
        'Motor brebet saat kondisi dingin biasanya karena busi atau setting udara belum optimal.'
    ),
    (
        'brebet', 
        'Motor brebet secara umum', 
        'Motor brebet dapat disebabkan oleh busi, karburator, injektor, atau filter udara.'
    ),
    (
        'mogok', 
        'Motor mogok / mati mendadak', 
        'Motor mogok bisa disebabkan aki lemah, busi bermasalah, suplai bensin tidak lancar, atau sistem pengapian terganggu.'
    ),
    (
        'rem', 
        'Masalah rem motor', 
        'Masalah rem bisa disebabkan kampas rem aus, setelan rem kurang tepat, atau komponen rem perlu dibersihkan.'
    ),
    (
        'asap', 
        'Asap putih dari knalpot', 
        'Asap putih dari motor biasanya berkaitan dengan oli yang ikut terbakar atau kondisi mesin yang perlu diperiksa.'
    ),
    (
        'bensin', 
        'Kehabisan bensin atau masalah bahan bakar', 
        'Jika motor kehabisan bensin, isi bahan bakar terlebih dahulu lalu coba starter ulang. Jika tetap bermasalah, sistem bahan bakar perlu dicek.'
    ),
    (
        'bunyi', 
        'Bunyi tidak normal pada motor', 
        'Bunyi tidak normal pada motor bisa berasal dari rantai, CVT, rem, atau bagian mesin. Sebaiknya dicek langsung agar sumber bunyinya jelas.'
    )
]

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
