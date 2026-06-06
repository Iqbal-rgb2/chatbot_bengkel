import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'database' / 'chatbot.db'

# Baca data dari berkas JSON
JSON_PATH = BASE_DIR / 'scripts' / 'seeder_data' / 'barang_spareparts.json'
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_categories = data['new_categories']
new_items = [(item['nama_barang'], item['kategori'], item['harga'], item['stok']) for item in data['new_items']]

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT nama_kategori FROM kategori_barang")
    existing_categories = {row[0].lower() for row in cursor.fetchall()}

    inserted_categories = 0
    for kategori in new_categories:
        if kategori.lower() not in existing_categories:
            cursor.execute(
                "INSERT INTO kategori_barang (nama_kategori) VALUES (?)",
                (kategori,)
            )
            inserted_categories += 1

    cursor.execute("SELECT LOWER(nama_barang) FROM barang")
    existing_barang = {row[0] for row in cursor.fetchall()}

    inserted_items = 0
    for nama_barang, kategori, harga, stok in new_items:
        if nama_barang.lower() not in existing_barang:
            cursor.execute(
                "INSERT INTO barang (nama_barang, kategori, harga, stok, cocok_untuk) VALUES (?, ?, ?, ?, ?)",
                (nama_barang, kategori, harga, stok, '')
            )
            inserted_items += 1

    conn.commit()

print(f'Inserted categories: {inserted_categories}')
print(f'Inserted barang items: {inserted_items}')
