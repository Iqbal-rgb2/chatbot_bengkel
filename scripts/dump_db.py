import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')
SQL_PATH = os.path.join(BASE_DIR, 'database', 'schema_and_seed.sql')

def dump_database():
    if not os.path.exists(DB_PATH):
        print(f"Database tidak ditemukan di {DB_PATH}")
        return

    print("Melakukan dump database SQLite...")
    conn = sqlite3.connect(DB_PATH)
    
    with open(SQL_PATH, 'w', encoding='utf-8') as f:
        for line in conn.iterdump():
            # Kita skip log chat dan riwayat stok dari backup agar tidak mengotori repositori
            if "INSERT INTO \"log_chat\"" in line or "INSERT INTO \"riwayat_stok\"" in line:
                continue
            f.write(f"{line}\n")
            
    conn.close()
    print(f"Dump database berhasil disimpan ke {SQL_PATH}")

if __name__ == "__main__":
    dump_database()
