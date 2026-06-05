import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all logs that need classification
    cursor.execute("""
        SELECT id_chat, intent FROM log_chat WHERE klasifikasi IS NULL OR klasifikasi = ''
    """)
    rows = cursor.fetchall()

    print(f"Found {len(rows)} logs to classify.")

    updated_count = 0
    for id_chat, intent in rows:
        if intent == 'fallback_bengkel':
            klasifikasi = 'lingkup_bengkel_belum_ada'
        elif intent in ['fallback_luar_bengkel', 'sarkasme_kasar', 'fallback']:
            klasifikasi = 'melenceng'
        else:
            klasifikasi = 'ada_di_database'

        cursor.execute("""
            UPDATE log_chat
            SET klasifikasi = ?
            WHERE id_chat = ?
        """, (klasifikasi, id_chat))
        updated_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully migrated {updated_count} logs.")

if __name__ == '__main__':
    migrate()
