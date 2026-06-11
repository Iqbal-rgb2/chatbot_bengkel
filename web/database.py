import sqlite3
from flask import session
from web.config import DATABASE_PATH

def get_db_connection():
    conn = sqlite3.connect(
        DATABASE_PATH
    )
    conn.row_factory = sqlite3.Row
    return conn

def simpan_riwayat_stok(
    cursor,
    id_barang,
    aksi,
    stok_lama,
    stok_baru
):
    id_admin = session.get(
        'id_admin'
    )

    if id_admin is None:
        username = session.get(
            'username'
        )

        cursor.execute(
            """
            SELECT id_admin
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        if user:
            id_admin = user[0]

    if id_admin is None:
        return

    cursor.execute(
        """
        INSERT INTO riwayat_stok
        (
            id_admin,
            id_barang,
            aksi,
            stok_lama,
            stok_baru
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            id_admin,
            id_barang,
            aksi,
            stok_lama,
            stok_baru
        )
    )

def simpan_log_chat(
    pertanyaan,
    pertanyaan_normalisasi,
    intent,
    jawaban
):
    # Skip saving logs during automated testing to avoid polluting the database
    try:
        from flask import current_app
        if current_app and current_app.testing:
            return
    except RuntimeError:
        pass

    # Klasifikasi otomatis
    if intent == 'fallback_bengkel':
        klasifikasi = 'lingkup_bengkel_belum_ada'
    elif intent in ['fallback_luar_bengkel', 'sarkasme_kasar', 'fallback']:
        klasifikasi = 'melenceng'
    else:
        klasifikasi = 'ada_di_database'

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO log_chat
        (
            pertanyaan,
            pertanyaan_normalisasi,
            intent,
            jawaban,
            klasifikasi
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            pertanyaan,
            pertanyaan_normalisasi,
            intent,
            jawaban,
            klasifikasi
        )
    )

    conn.commit()
    conn.close()
