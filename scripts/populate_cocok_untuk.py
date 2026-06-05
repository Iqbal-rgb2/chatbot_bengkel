import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Map id_barang to the suitable motor models (cocok_untuk)
mappings = {
    16: 'mio, beat, vario',             # Knalpot Racing Proliner
    17: 'beat, vario, scoopy',           # Knalpot Standar
    18: 'mio, fino, nmax, aerox',        # Spion Mio
    19: 'vario, beat, scoopy, pcx',      # Spion Vario 125
    20: 'beat, vario, scoopy, pcx',      # Filter Oli AHM
    21: 'mio, nmax, aerox',              # Filter Oli Yamalube
    22: 'mio, beat, vario, scoopy, nmax',# Kampas Kopling Matic
    23: 'supra, jupiter, vega',          # Kampas Kopling Bebek
    24: 'mio, beat, scoopy',             # Roller CVT 15x12
    25: 'vario, nmax, aerox, pcx',       # Roller CVT 16x13
    26: 'mio, fino',                     # CDI Yamaha Mio
    27: 'beat, scoopy',                  # CDI Honda Beat
    28: 'supra, jupiter, vega, beat, mio',# Kabel Busi
    29: 'vixion, cb150r, supra',         # Kabel Kopling
    30: 'mio, beat, vario, scoopy, supra',# Karet Gas
    31: 'beat, vario, scoopy, mio',      # Switch Starter
    32: 'nmax, pcx, vario',              # Relay Starter
    33: 'mio, jupiter, vega',            # Karburator Yamaha
    34: 'beat, supra, revo',             # Karburator Honda
    35: 'supra, jupiter, vega, rx king', # Rantai SSS 428
    36: 'mio, beat, vario, scoopy',      # Velg Depan
    37: 'mio, beat, vario, scoopy',      # Velg Belakang
    38: 'beat, vario, scoopy, mio, nmax',# Lampu Depan LED
    39: 'beat, vario, scoopy, mio, nmax, pcx', # Lampu Sen LED
    40: 'beat, vario, scoopy, mio, nmax, pcx', # Kampas Rem Cakram
    41: 'beat, vario, scoopy, mio',      # Cakram Depan
    42: 'beat, vario, mio, nmax',        # Master Rem Depan
    43: 'beat, vario, scoopy, mio',      # Shockbreaker Depan
    44: 'beat, vario, scoopy, mio, nmax',# Shockbreaker Belakang
    45: 'beat, vario, scoopy',           # Busi NGK KR7A
    46: 'nmax, pcx, aerox'               # Aki Yuasa YTX7A-BS
}

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
