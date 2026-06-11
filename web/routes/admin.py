import os
import sqlite3
import json
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import check_password_hash
from web.config import DATABASE_PATH
from web.database import simpan_riwayat_stok

admin_bp = Blueprint('admin', __name__)

# =====================================
# LOGIN PETUGAS
# =====================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id_admin, password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['login'] = True
            session['username'] = username
            session['id_admin'] = user[0]
            return redirect(url_for('admin.dashboard_barang'))
        else:
            error = "Username atau password salah."

    return render_template(
        'login.html',
        error=error
    )

# =====================================
# DASHBOARD BARANG
# =====================================
@admin_bp.route('/dashboard_barang')
def dashboard_barang():
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_barang, nama_barang, kategori, harga, stok, cocok_untuk
        FROM barang
    """)
    data_barang = cursor.fetchall()

    cursor.execute("""
        SELECT nama_kategori
        FROM kategori_barang
        ORDER BY nama_kategori
    """)
    data_kategori = cursor.fetchall()
    conn.close()

    return render_template(
        'dashboard_barang.html',
        data_barang=data_barang,
        data_kategori=data_kategori
    )

# =====================================
# RIWAYAT STOK
# =====================================
@admin_bp.route('/riwayat_stok')
def riwayat_stok():
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT riwayat_stok.id_riwayat,
               users.username,
               barang.nama_barang,
               riwayat_stok.aksi,
               riwayat_stok.stok_lama,
               riwayat_stok.stok_baru,
               riwayat_stok.tanggal
        FROM riwayat_stok
        LEFT JOIN users
            ON riwayat_stok.id_admin = users.id_admin
        LEFT JOIN barang
            ON riwayat_stok.id_barang = barang.id_barang
        ORDER BY riwayat_stok.id_riwayat DESC
    """)
    data_riwayat = cursor.fetchall()
    conn.close()

    return render_template(
        'riwayat_stok.html',
        data_riwayat=data_riwayat
    )

# =====================================
# LOG CHAT
# =====================================
@admin_bp.route('/log_chat')
def log_chat():
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_chat,
               pertanyaan,
               pertanyaan_normalisasi,
               intent,
               jawaban,
               waktu,
               klasifikasi
        FROM log_chat
        ORDER BY id_chat DESC
    """)
    data_log_chat = cursor.fetchall()
    conn.close()

    return render_template(
        'log_chat.html',
        data_log_chat=data_log_chat
    )

# =====================================
# PERFORMA & EVALUASI CHATBOT
# =====================================
@admin_bp.route('/performa')
def performa():
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    metrics_path = os.path.join(current_app.root_path, '..', 'data', 'processed', 'metrics.json')
    metrics = None
    lowest_info = None

    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
        except Exception as e:
            print(f"Error loading metrics.json: {e}")

    if metrics and 'classification_report' in metrics:
        try:
            lowest_intent = None
            lowest_f1 = 1.1
            for key, val in metrics['classification_report'].items():
                if key not in ['accuracy', 'macro avg', 'weighted avg']:
                    f1 = val.get('f1-score', 1.0)
                    if f1 < lowest_f1:
                        lowest_f1 = f1
                        lowest_intent = key
            
            if lowest_intent:
                intent_mapping = {
                    'akhir_percakapan': {
                        'friendly_name': 'Ucapan Terima Kasih',
                        'explanation': 'Kata penutup atau penutup pembicaraan biasanya hanya berupa kata-kata sangat singkat (contoh: "oke", "bye", "makasih", "cukup"). Kata-kata pendek ini memiliki sedikit petunjuk huruf/kata (fitur TF-IDF minim), sehingga model Naive Bayes kadang keliru memprediksinya sebagai sapaan pembuka atau menu bantuan. Hal ini sangat wajar terjadi dalam pemrosesan bahasa alami (NLP).'
                    },
                    'sapaan': {
                        'friendly_name': 'Sapaan & Salam Pembuka',
                        'explanation': 'Sapaan pembuka seperti "halo", "siang min", atau "permisi" sangat pendek dan sering kali tumpang tindih dengan sapaan di topik lain. Tanpa adanya kata kunci spesifik bengkel (seperti "servis" atau "stok"), pembobotan TF-IDF menghasilkan nilai probabilitas yang mirip antar kategori sapaan, bantuan, atau kontak admin, sehingga kestabilannya cenderung dinamis.'
                    },
                    'kontak_admin': {
                        'friendly_name': 'Kontak Admin (WhatsApp)',
                        'explanation': 'Pertanyaan terkait kontak admin sering kali mengandung kata kunci yang mirip dengan menu bantuan umum (seperti "admin", "bantuan", "petugas", "chat"). Karakteristik kata kunci yang tumpang tindih ini menyebabkan algoritma klasifikasi Naive Bayes rentan salah membedakan antara kebutuhan menu bantuan umum dengan permintaan kontak WhatsApp admin secara langsung.'
                    },
                    'bantuan_umum': {
                        'friendly_name': 'Menu Bantuan Chatbot',
                        'explanation': 'Topik bantuan umum bersifat sangat luas dan sering kali menjadi "tempat penampungan" bagi kata-kata tanya yang umum. Karena tidak memiliki fitur kata kunci yang unik dan spesifik dibanding topik bengkel lainnya, model Naive Bayes kesulitan menempatkan probabilitas tinggi pada kelas ini secara konsisten.'
                    },
                    'cek_stok': {
                        'friendly_name': 'Cek Stok Barang',
                        'explanation': 'Pertanyaan mengenai stok barang (seperti "ready?", "ada oli?", "busi ada?") sering kali sangat mirip dengan "Detail Informasi Barang" atau "Daftar Semua Barang". Kata kunci seperti nama suku cadang ("oli", "busi", "ban") muncul di ketiga topik tersebut, sehingga model Naive Bayes kadang mengalami bias klasifikasi antar kategori produk tersebut.'
                    },
                    'info_barang': {
                        'friendly_name': 'Detail Informasi Barang',
                        'explanation': 'Detail informasi barang sering kali menanyakan harga atau spesifikasi suatu produk (misal: "berapa harga ban?", "spesifikasi oli mpx2"). Keberadaan kata nama barang yang beririsan dengan topik "Cek Stok" membuat pembobotan TF-IDF menghasilkan kemiripan kosinus (Cosine Similarity) yang berdekatan, berpotensi menurunkan tingkat presisi.'
                    },
                    'daftar_barang': {
                        'friendly_name': 'Daftar Semua Barang',
                        'explanation': 'Pertanyaan daftar barang meminta list produk (misal: "daftar oli yang ada apa saja?"). Karena menggunakan kata kunci barang yang juga digunakan pada topik stok dan info barang, model Naive Bayes dapat keliru mengelompokkannya jika pengguna tidak menuliskan kata perintah "daftar" atau "list" dengan jelas.'
                    },
                    'layanan_servis': {
                        'friendly_name': 'Diagnosa Keluhan Motor',
                        'explanation': 'Topik keluhan motor menggunakan deskripsi masalah fisik (seperti "mogok", "brebet", "rem", "mesin", "bensin", "asap", "bunyi", "tektek") yang kosakatanya sangat variatif. Variasi bahasa informal pelanggan yang tidak terduga membuat representasi vektor TF-IDF pada data uji kadang tidak terwakili sepenuhnya pada data latih, memicu salah klasifikasi.'
                    },
                    'harga_servis': {
                        'friendly_name': 'Biaya Servis & Jasa',
                        'explanation': 'Pertanyaan biaya servis menanyakan tarif (misal: "ganti ban kena berapa?", "ongkos tune up"). Jika pelanggan hanya menuliskan nama tindakan tanpa nominal atau kata tanya harga yang jelas, model Naive Bayes sering kali bias dan mengarahkannya ke kategori diagnosa layanan servis umum.'
                    },
                    'jadwal_bengkel': {
                        'friendly_name': 'Jadwal Buka Bengkel',
                        'explanation': 'Pertanyaan jadwal mencakup hari dan jam operasional. Apabila pengguna menanyakan hari dengan kalimat sangat kasual (seperti "hari ini buka?"), kata "hari" dan "buka" kadang terdeteksi mirip dengan sapaan waktu atau bantuan, yang dapat sedikit menurunkan performa recall.'
                    },
                    'lokasi_bengkel': {
                        'friendly_name': 'Alamat & Peta Lokasi',
                        'explanation': 'Meskipun topik lokasi biasanya memiliki akurasi tinggi karena kata kunci "alamat", "rute", "maps", atau "lokasi" yang sangat spesifik, performa dapat menurun apabila pelanggan bertanya menggunakan nama wilayah atau patokan jalan unik yang belum terdaftar di data latih chatbot.'
                    },
                    'rekom_produk': {
                        'friendly_name': 'Rekomendasi Oli & Suku Cadang',
                        'explanation': 'Topik rekomendasi menanyakan produk terbaik (misal: "oli yang bagus buat beat apa?"). Kemiripan struktur kalimat rekomendasi dengan detail informasi barang atau keluhan mesin membuat probabilitas kelas ini kadang beririsan tipis pada klasifikasi Naive Bayes.'
                    }
                }
                lowest_info = intent_mapping.get(lowest_intent, {
                    'friendly_name': lowest_intent,
                    'explanation': 'Topik ini memiliki performa terendah pada evaluasi saat ini karena keterbatasan representasi kata kunci unik atau variasi input uji yang melampaui pola data latih.'
                })
        except Exception as ex:
            print(f"Error calculating lowest metric: {ex}")

    return render_template(
        'performa.html',
        metrics=metrics,
        lowest_info=lowest_info
    )

# =====================================
# UPDATE KLASIFIKASI LOG CHAT
# =====================================
@admin_bp.route('/update_klasifikasi_chat/<int:id>', methods=['POST'])
def update_klasifikasi_chat(id):
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    klasifikasi = request.form.get('klasifikasi')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE log_chat
        SET klasifikasi = ?
        WHERE id_chat = ?
        """,
        (klasifikasi, id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('admin.log_chat'))

# =====================================
# HAPUS LOG CHAT (Hanya untuk klasifikasi 'melenceng')
# =====================================
@admin_bp.route('/delete_log_chat/<int:id>', methods=['POST'])
def delete_log_chat(id):
    if 'login' not in session:
        return {"status": "error", "message": "Unauthorized"}, 401

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT klasifikasi FROM log_chat WHERE id_chat = ?",
        (id,)
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"status": "error", "message": "Log tidak ditemukan"}, 404

    klasifikasi = row[0]
    if klasifikasi != 'melenceng':
        conn.close()
        return {"status": "error", "message": "Hanya log dengan klasifikasi 'melenceng' yang dapat dihapus"}, 400

    cursor.execute(
        "DELETE FROM log_chat WHERE id_chat = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Log chat melenceng berhasil dihapus"}, 200

# =====================================
# HAPUS SEMUA LOG CHAT MELENCENG
# =====================================
@admin_bp.route('/delete_all_melenceng_chat', methods=['POST'])
def delete_all_melenceng_chat():
    if 'login' not in session:
        return {"status": "error", "message": "Unauthorized"}, 401

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM log_chat WHERE klasifikasi = 'melenceng'"
    )
    count = cursor.fetchone()[0]

    if count == 0:
        conn.close()
        return {"status": "error", "message": "Tidak ada log chat melenceng untuk dihapus"}, 400

    cursor.execute(
        "DELETE FROM log_chat WHERE klasifikasi = 'melenceng'"
    )
    conn.commit()
    conn.close()

    return {"status": "success", "message": f"{count} log chat melenceng berhasil dihapus"}, 200

# =====================================
# TAMBAH BARANG
# =====================================
@admin_bp.route('/tambah_barang', methods=['POST'])
def tambah_barang():
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    nama_barang = request.form.get('nama_barang')
    kategori = request.form.get('kategori')
    harga = request.form.get('harga')
    stok = request.form.get('stok')
    cocok_untuk = request.form.get('cocok_untuk')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO barang (nama_barang, kategori, harga, stok, cocok_untuk)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nama_barang, kategori, harga, stok, cocok_untuk)
    )
    id_barang = cursor.lastrowid

    simpan_riwayat_stok(
        cursor,
        id_barang,
        'tambah_barang',
        None,
        stok
    )
    conn.commit()
    conn.close()

    return redirect(url_for('admin.dashboard_barang'))

# =====================================
# EDIT BARANG
# =====================================
@admin_bp.route('/edit_barang/<int:id>', methods=['POST'])
def edit_barang(id):
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    nama_barang = request.form.get('nama_barang')
    kategori = request.form.get('kategori')
    harga = request.form.get('harga')
    stok = request.form.get('stok')
    cocok_untuk = request.form.get('cocok_untuk')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT stok
        FROM barang
        WHERE id_barang = ?
        """,
        (id,)
    )
    data_lama = cursor.fetchone()
    stok_lama = data_lama[0] if data_lama else None

    cursor.execute(
        """
        UPDATE barang
        SET nama_barang = ?, kategori = ?, harga = ?, stok = ?, cocok_untuk = ?
        WHERE id_barang = ?
        """,
        (nama_barang, kategori, harga, stok, cocok_untuk, id)
    )

    simpan_riwayat_stok(
        cursor,
        id,
        'edit_barang',
        stok_lama,
        stok
    )
    conn.commit()
    conn.close()

    return redirect(url_for('admin.dashboard_barang'))

# =====================================
# HAPUS BARANG
# =====================================
@admin_bp.route('/hapus_barang/<int:id>')
def hapus_barang(id):
    if 'login' not in session:
        return redirect(url_for('admin.login'))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT stok
        FROM barang
        WHERE id_barang = ?
        """,
        (id,)
    )
    data_lama = cursor.fetchone()
    stok_lama = data_lama[0] if data_lama else None

    cursor.execute(
        """
        DELETE FROM barang
        WHERE id_barang = ?
        """,
        (id,)
    )

    simpan_riwayat_stok(
        cursor,
        id,
        'hapus_barang',
        stok_lama,
        0
    )
    conn.commit()
    conn.close()

    return redirect(url_for('admin.dashboard_barang'))

# =====================================
# LOGOUT
# =====================================
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))
