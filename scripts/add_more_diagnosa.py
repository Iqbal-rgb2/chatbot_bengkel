import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Baca data diagnosa tambahan dari berkas JSON
JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'seeder_data', 'new_diagnosa.json')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    diagnosa_data = json.load(f)
new_diagnosa = [(item['kata_kunci'], item['gejala'], item['solusi_analisis']) for item in diagnosa_data]

inserted_count = 0
for kata_kunci, gejala, solusi in new_diagnosa:
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

print(f"Berhasil menambahkan {inserted_count} data diagnosa tambahan ke database.")
