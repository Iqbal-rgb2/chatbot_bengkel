import sqlite3
import os

# =========================
# PATH
# =========================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    'database',
    'chatbot.db'
)

# =========================
# CONNECT DATABASE
# =========================
conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# =========================
# BUAT TABEL RIWAYAT STOK
# =========================
cursor.execute('''
CREATE TABLE IF NOT EXISTS riwayat_stok (

    id_riwayat INTEGER PRIMARY KEY AUTOINCREMENT,

    id_admin INTEGER NOT NULL,

    id_barang INTEGER NOT NULL,

    aksi TEXT NOT NULL,

    stok_lama INTEGER,

    stok_baru INTEGER,

    tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_admin) REFERENCES users(id_admin),

    FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
)
''')

# =========================
# BUAT TABEL LOG CHAT
# =========================
cursor.execute('''
CREATE TABLE IF NOT EXISTS log_chat (

    id_chat INTEGER PRIMARY KEY AUTOINCREMENT,

    pertanyaan TEXT NOT NULL,

    pertanyaan_normalisasi TEXT,

    intent TEXT,

    jawaban TEXT,

    waktu DATETIME DEFAULT CURRENT_TIMESTAMP,

    klasifikasi TEXT
)
''')

cursor.execute(
    "PRAGMA table_info(log_chat)"
)

kolom_log_chat = [
    row[1]
    for row in cursor.fetchall()
]

if 'klasifikasi' not in kolom_log_chat:

    cursor.execute(
        "ALTER TABLE log_chat ADD COLUMN klasifikasi TEXT"
    )

if 'pertanyaan_normalisasi' not in kolom_log_chat:

    cursor.execute(
        "ALTER TABLE log_chat ADD COLUMN pertanyaan_normalisasi TEXT"
    )

# =========================
# SIMPAN DATABASE
# =========================
conn.commit()

print("Tabel tambahan berhasil disiapkan!")

# =========================
# CLOSE
# =========================
conn.close()
