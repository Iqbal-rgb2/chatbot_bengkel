import sqlite3
import os
import sys
import argparse
from pathlib import Path

# =========================
# PATH CONFIGURATION
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'database' / 'chatbot.db'
SQL_PATH = BASE_DIR / 'database' / 'schema_and_seed.sql'

def init_db():
    """Menginisialisasi database dengan menjalankan berkas schema_and_seed.sql"""
    print("Mereset dan menginisialisasi database dari schema_and_seed.sql...")
    
    # Hapus database lama jika ada agar bersih
    if DB_PATH.exists():
        try:
            os.remove(DB_PATH)
            print(f"File database lama {DB_PATH.name} berhasil dihapus.")
        except Exception as e:
            print(f"Gagal menghapus database lama: {e}")
            sys.exit(1)
            
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    if SQL_PATH.exists():
        with open(SQL_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        try:
            cursor.executescript(sql_script)
            conn.commit()
            print("Inisialisasi skema dan data database berhasil!")
        except sqlite3.Error as e:
            print(f"Gagal mengeksekusi skema database: {e}")
            conn.rollback()
            conn.close()
            sys.exit(1)
    else:
        print(f"Error: File skema {SQL_PATH} tidak ditemukan.")
        conn.close()
        sys.exit(1)
        
    # Pastikan tabel tambahan riwayat_stok, log_chat, dan diagnosa_keluhan siap
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diagnosa_keluhan (
        id_diagnosa INTEGER PRIMARY KEY AUTOINCREMENT,
        kata_kunci TEXT NOT NULL UNIQUE,
        gejala TEXT NOT NULL,
        solusi_analisis TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    print("Database berhasil diinisialisasi dan dikonfigurasi!")

def dump_db():
    """Mengekspor seluruh database ke dalam berkas schema_and_seed.sql untuk backup"""
    if not DB_PATH.exists():
        print(f"Error: Database {DB_PATH.name} tidak ditemukan.")
        return

    print("Mengekspor database SQLite ke schema_and_seed.sql...")
    conn = sqlite3.connect(str(DB_PATH))
    
    try:
        with open(SQL_PATH, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                # Kita lewati insert log_chat dan riwayat_stok agar cadangan bersih
                if "INSERT INTO \"log_chat\"" in line or "INSERT INTO \"riwayat_stok\"" in line:
                    continue
                f.write(f"{line}\n")
        print(f"Dump database berhasil disimpan ke {SQL_PATH.name}")
    except Exception as e:
        print(f"Gagal melakukan dump database: {e}")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="Pusat Pengelola Database Chatbot Kurnia Motor")
    parser.add_argument('--init', action='store_true', help="Hapus database lama dan buat skema & data database baru dari SQL")
    parser.add_argument('--dump', action='store_true', help="Backup isi database ke dalam schema_and_seed.sql")
    
    args = parser.parse_args()
    
    # Jika tidak ada argumen, tampilkan bantuan
    if not (args.init or args.dump):
        parser.print_help()
        sys.exit(0)
        
    if args.init:
        init_db()
    if args.dump:
        dump_db()

if __name__ == "__main__":
    main()
