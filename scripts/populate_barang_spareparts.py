import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'database' / 'chatbot.db'

new_categories = [
    'filter oli',
    'kampas kopling',
    'knalpot',
    'spion',
    'roller',
    'switch',
    'starter motor',
    'karburator',
    'cdi',
    'rem cakram',
    'velg',
    'sparepart',
    'rantai',
    'lampu'
]

new_items = [
    ('Knalpot Racing Proliner', 'knalpot', 450000, 6),
    ('Knalpot Standar', 'knalpot', 250000, 5),
    ('Spion Mio', 'spion', 32000, 12),
    ('Spion Vario 125', 'spion', 35000, 8),
    ('Filter Oli AHM', 'filter oli', 28000, 15),
    ('Filter Oli Yamalube', 'filter oli', 30000, 10),
    ('Kampas Kopling Matic', 'kampas kopling', 90000, 7),
    ('Kampas Kopling Bebek', 'kampas kopling', 85000, 6),
    ('Roller CVT 15x12', 'roller', 45000, 14),
    ('Roller CVT 16x13', 'roller', 47000, 10),
    ('CDI Yamaha Mio', 'cdi', 150000, 5),
    ('CDI Honda Beat', 'cdi', 155000, 4),
    ('Kabel Busi', 'sparepart', 20000, 20),
    ('Kabel Kopling', 'sparepart', 25000, 18),
    ('Karet Gas', 'sparepart', 17000, 15),
    ('Switch Starter', 'switch', 40000, 10),
    ('Relay Starter', 'switch', 50000, 5),
    ('Karburator Yamaha', 'karburator', 325000, 2),
    ('Karburator Honda', 'karburator', 340000, 3),
    ('Rantai SSS 428', 'rantai', 155000, 9),
    ('Velg Depan', 'velg', 400000, 2),
    ('Velg Belakang', 'velg', 450000, 2),
    ('Lampu Depan LED', 'lampu', 120000, 10),
    ('Lampu Sen LED', 'lampu', 45000, 10),
    ('Kampas Rem Cakram', 'rem cakram', 65000, 12),
    ('Cakram Depan', 'rem cakram', 120000, 4),
    ('Master Rem Depan', 'rem cakram', 175000, 3),
    ('Shockbreaker Depan', 'sparepart', 250000, 6),
    ('Shockbreaker Belakang', 'sparepart', 270000, 5),
    ('Busi NGK KR7A', 'busi', 26000, 15),
    ('Aki Yuasa YTX7A-BS', 'aki', 300000, 5)
]

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
