import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Baca data pemetaan cocok_untuk dari berkas JSON
JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'seeder_data', 'cocok_untuk.json')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
mappings = {int(k): v for k, v in json_data.items()}

updated_count = 0
for id_barang, cocok_untuk in mappings.items():
    cursor.execute(
        "UPDATE barang SET cocok_untuk = ? WHERE id_barang = ?",
        (cocok_untuk, id_barang)
    )
    if cursor.rowcount > 0:
        updated_count += 1

conn.commit()
conn.close()

print(f"Berhasil memperbarui data dummy cocok_untuk untuk {updated_count} barang.")
