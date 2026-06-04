import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in chatbot.db:")
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    count = cursor.fetchone()[0]
    print(f"- {t}: {count} rows")
    
    # Get columns
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [f"{row[1]} ({row[2]})" for row in cursor.fetchall()]
    print(f"  Columns: {', '.join(cols)}")

conn.close()
