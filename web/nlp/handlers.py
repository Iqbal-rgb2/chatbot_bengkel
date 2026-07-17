import re
from flask import session
from web.database import get_db_connection

# =====================================
# KONSTANTA SUKU CADANG MOTOR
# =====================================
PART_KEYWORDS = {
    "oli", "busi", "aki", "accu", "ban", "rem", "kampas", "cakram", "kaliper", "tromol",
    "kopling", "gasket", "paking", "rantai", "velg", "pelek", "spion", "knalpot",
    "lampu", "klakson", "filter", "roller", "switch", "karburator", "karbu", "cdi",
    "ecu", "sekring", "fuse", "starter", "piston", "seher", "klep", "noken",
    "shock", "shockbreaker", "injektor", "radiator", "coolant", "spidometer",
    "speedometer", "dinamo", "koil", "spul", "kiprok", "cangklong", "cvt",
    "mesin", "injeksi", "stang", "setang", "komstir", "suspensi",
    "spakbor", "slebor", "fender", "mika", "reflektor", "bohlam", "led",
    "gir", "gear", "vanbelt", "vbelt", "kamprat", "keteng", "as", "kabel", "skok"
}

TIDAK_DISEDIAKAN_PARTS = {
    "knalpot", "velg", "pelek", "spion", "klakson", "spakbor", "slebor",
    "fender", "mika", "reflektor", "bohlam", "led"
}

def get_user_part_keyword(text):
    words = set(re.findall(r'[a-zA-Z0-9]+', text.lower()))
    user_parts = words.intersection(PART_KEYWORDS)
    if user_parts:
        return list(user_parts)[0]
    return None

def get_user_descriptors(text):
    COMMON_STOPWORDS = {
        "apakah", "ada", "di", "sini", "saya", "mau", "beli", "jual", "ready", "stok", 
        "bengkel", "motor", "yang", "untuk", "dan", "atau", "buat", "kah", "ga", "gak", 
        "adakah", "punya", "cari", "tanya", "info", "harga", "seberapa", "berapa", 
        "siap", "sedia", "permisi", "hallo", "halo", "tolong", "bisa", "cek", "kurnia",
        "mas", "mbak", "bos", "gan", "kak", "min", "apa", "saja", "sebutkan", 
        "tampilkan", "daftar", "pilihan", "semua", "yg", "ada", "yang", "tersedia"
    }
    words = set(re.findall(r'[a-zA-Z0-9]+', text.lower()))
    return words - COMMON_STOPWORDS - PART_KEYWORDS

# =====================================
# FORMAT HTML TABLE HELPER
# =====================================
def format_barang_table(results, show_kategori=False, show_price_stock=True):
    html = '<div class="chat-table-container"><table class="chat-table">'
    html += '<thead><tr>'
    html += '<th style="text-align: left;">Nama Barang</th>'

    has_kategori = False
    if results and 'kategori' in results[0].keys():
        has_kategori = show_kategori

    if has_kategori:
        html += '<th style="text-align: left;">Kategori</th>'
    if show_price_stock:
        html += '<th style="text-align: left;">Stok</th>'
        html += '<th style="text-align: left;">Harga</th>'
    html += '</tr></thead><tbody>'

    for row in results:
        html += '<tr>'
        html += f'<td>{row["nama_barang"]}</td>'
        if has_kategori:
            html += f'<td>{row["kategori"].capitalize()}</td>'
        if show_price_stock:
            stok = row["stok"]
            harga = row["harga"]
            html += f'<td>{stok} pcs</td>'
            html += f'<td>Rp{harga:,}</td>'
        html += '</tr>'

    html += '</tbody></table></div>'
    return html

# =====================================
# CONVERSATIONAL FOLLOW-UP SUGGESTIONS
# =====================================
def add_conversational_follow_up(intent, response, normalized_input):
    suggestions = []
    follow_up_text = ""

    text = normalized_input.lower()

    if intent == "layanan_servis":
        if "brebet" in text:
            follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan sparepart terkait (seperti busi, karburator, filter udara) atau melihat estimasi biaya servis?"
            suggestions = ["Cek Stok Busi", "Cek Stok Karburator", "Biaya Servis Lengkap"]
        elif "mogok" in text:
            follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan aki/busi, atau ingin langsung menghubungi petugas bengkel kami?"
            suggestions = ["Cek Stok Aki", "Cek Stok Busi", "Hubungi WhatsApp"]
        elif "rem" in text:
            follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan kampas rem atau memeriksa biaya ganti kampas rem?"
            suggestions = ["Cek Kampas Rem", "Biaya Servis Rem", "Lokasi Bengkel"]
        elif "cvt" in text or "roller" in text or "van belt" in text or "belt" in text:
            follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan sparepart CVT (seperti roller, v-belt) atau menanyakan biaya servis CVT?"
            suggestions = ["Cek Roller CVT", "Cek CVT Belt", "Biaya Servis Ringan"]
        else:
            follow_up_text = "<br><br>Apakah Anda ingin berkonsultasi lebih lanjut dengan mekanik kami via WhatsApp, atau memeriksa biaya servis?"
            suggestions = ["Hubungi WhatsApp", "Biaya Servis Lengkap", "Lokasi Bengkel"]

    elif intent in ["rekom_produk", "daftar_barang"]:
        motor = None
        for m in ["beat", "vario", "mio", "nmax", "scoopy", "pcx", "supra"]:
            if m in text:
                motor = m.capitalize()
                break

        kategori = None
        for k in ["oli", "ban", "aki", "busi", "kampas", "roller", "rantai"]:
            if k in text:
                kategori = k
                break

        if motor and kategori:
            follow_up_text = f"<br><br>Apakah Anda ingin mengecek ketersediaan stok {kategori} untuk motor {motor} saat ini?"
            suggestions = [f"Stok {kategori} {motor}", f"Biaya Servis {motor}", "Lokasi Bengkel"]
        elif motor:
            follow_up_text = f"<br><br>Apakah Anda ingin mengecek ketersediaan stok suku cadang khusus untuk motor {motor}?"
            suggestions = [f"Stok barang {motor}", f"Biaya Servis {motor}", "Lokasi Bengkel"]
        elif kategori:
            follow_up_text = f"<br><br>Apakah Anda ingin menanyakan produk {kategori} yang cocok untuk tipe motor Anda?"
            suggestions = [f"Oli yang cocok untuk Beat", f"Ban yang cocok untuk Vario", "Biaya Ganti Oli"]
        else:
            follow_up_text = "<br><br>Apakah Anda ingin mencari rekomendasi sparepart untuk tipe motor tertentu?"
            suggestions = ["Oli untuk Beat", "Ban untuk Vario", "Kampas Rem Supra"]

    elif intent in ["cek_stok", "info_barang"]:
        motor = None
        for m in ["beat", "vario", "mio", "nmax", "scoopy", "pcx", "supra"]:
            if m in text:
                motor = m.capitalize()
                break
        if motor:
            follow_up_text = f"<br><br>Apakah Anda ingin menanyakan biaya jasa pasang/servis untuk motor {motor} di bengkel kami?"
            suggestions = [f"Biaya Servis {motor}", "Lokasi Bengkel", "Jam Buka Bengkel"]
        else:
            follow_up_text = "<br><br>Apakah Anda ingin berkonsultasi mengenai keluhan motor Anda atau menanyakan lokasi bengkel?"
            suggestions = ["Motor saya brebet", "Biaya Servis Motor", "Lokasi Bengkel"]

    elif intent == "lokasi_bengkel":
        follow_up_text = "<br><br>Apakah Anda ingin mengetahui jam buka/tutup operasional bengkel kami hari ini?"
        suggestions = ["Jam Buka Bengkel", "Hubungi WhatsApp", "Biaya Servis Motor"]

    elif intent == "jadwal_bengkel":
        follow_up_text = "<br><br>Apakah Anda membutuhkan petunjuk arah atau link rute Google Maps untuk menuju ke bengkel kami?"
        suggestions = ["Alamat & Rute Maps", "Hubungi WhatsApp", "Lokasi Bengkel"]

    elif intent == "harga_servis":
        follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan stok oli atau sparepart lainnya di bengkel kami?"
        suggestions = ["Cek Stok Oli", "Cek Stok Ban", "Jam Buka Bengkel"]

    elif intent in ["sapaan", "bantuan_umum"]:
        follow_up_text = "<br><br>Anda bisa menanyakan lokasi, jam buka, stok sparepart, atau mendiagnosa keluhan motor."
        suggestions = ["Jam Buka Bengkel", "Lokasi Bengkel", "Motor saya brebet", "Oli untuk Vario"]

    else:
        suggestions = ["Jam Buka Bengkel", "Lokasi Bengkel", "Biaya Servis Motor", "Hubungi WhatsApp"]

    return response + follow_up_text, suggestions

# =====================================
# CONVERSATIONAL CONTEXT CHECKER
# =====================================
def check_conversational_context(user_input):
    text = user_input.strip().lower()

    confirm_words = {
        "boleh", "iya", "ya", "mau", "oke", "ok", "silakan", "silahkan",
        "boleh dong", "kirim dong", "minta dong", "yup", "sip", "okey", "y",
        "boleh deh", "bolehdeh", "yo", "yoi", "mau dong", "mau ya", "tentu",
        "kirim", "minta", "oke deh", "okedeh", "yes", "yoa", "iy", "io",
        "ya dong", "yadong", "bolehlah", "boleh lah", "maulah", "mau lah",
        "siap", "siaap", "siappp", "kuy", "gas", "gaskan", "cuzz", "plis",
        "please", "ok deh", "ok dah", "oke dah", "okelah", "oke lah",
        "minta tolong", "tolong", "minta infonya", "infonya", "lakukan",
        "proses", "lanjut", "lanjutkan", "tentu saja", "tentunya", "please dong"
    }

    reject_words = {
        "tidak", "nggak", "ngga", "ga", "gak", "no", "engga", "enggak",
        "tidak usah", "ga usah", "g usah", "gosa", "gosaah", "no thanks",
        "nanti saja", "nanti", "belum", "g", "ndak", "nda", "ora", "ogah",
        "gamau", "ga mau", "nanti deh", "nanti aja", "nantiaja", "ntar",
        "ntar aja", "ntar saja", "tar aja", "skip", "cancel", "batal",
        "batalkan", "tidak perlu", "ga perlu", "ga usah deh", "g usah deh",
        "tidak usah deh", "gaperlu", "ndak usah", "nda usah"
    }

    if text in confirm_words:
        last_sug = session.get('last_suggestions')
        if last_sug and len(last_sug) > 0:
            target_query = last_sug[0]
            return target_query, None

    if text in reject_words:
        session.pop('last_suggestions', None)
        response = "Baik, silakan tanyakan hal lain jika ada yang ingin Anda ketahui tentang Bengkel Motor Kurnia. 😊"
        suggestions = ["Jam Buka Bengkel", "Lokasi Bengkel", "Biaya Servis Motor"]
        return None, (response, suggestions)

    return None, None

# =====================================
# DAFTAR BARANG TERSEDIA
# =====================================
def handle_list_barang(user_input):
    text = user_input.lower()
    words = set(re.findall(r'[a-zA-Z0-9]+', text))

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT nama_kategori FROM kategori_barang")
        kategori_barang = [row[0].lower() for row in cursor.fetchall() if row[0]]

        cursor.execute("SELECT DISTINCT LOWER(cocok_untuk) FROM barang")
        db_motors = set()
        for row in cursor.fetchall():
            if row[0]:
                for m in row[0].split(','):
                    motor_name = m.strip()
                    if motor_name:
                        db_motors.add(motor_name)

    selected_kategori = None
    for kategori in kategori_barang:
        kat_lower = kategori.lower()
        if ' ' in kat_lower:
            if kat_lower in text:
                selected_kategori = kategori
                break
        else:
            if kat_lower in words:
                selected_kategori = kategori
                break

    if not selected_kategori:
        for kategori in kategori_barang:
            kat_words = [w for w in kategori.split() if len(w) > 3]
            if kat_words and any(w in words for w in kat_words):
                selected_kategori = kategori
                break

    selected_motor = None
    sorted_motors = sorted(list(db_motors), key=len, reverse=True)
    for motor in sorted_motors:
        if motor in words:
            selected_motor = motor
            break

    with get_db_connection() as conn:
        cursor = conn.cursor()

        if selected_kategori and selected_motor:
            cursor.execute("""
                SELECT nama_barang, stok, harga
                FROM barang
                WHERE LOWER(kategori) = ?
                  AND LOWER(cocok_untuk) LIKE ?
                  AND stok > 0
                ORDER BY nama_barang
            """, (selected_kategori, f"%{selected_motor}%"))
        elif selected_kategori:
            cursor.execute("""
                SELECT nama_barang, stok, harga
                FROM barang
                WHERE LOWER(kategori) = ?
                  AND stok > 0
                ORDER BY nama_barang
            """, (selected_kategori,))
        elif selected_motor:
            cursor.execute("""
                SELECT nama_barang, stok, harga, kategori
                FROM barang
                WHERE LOWER(cocok_untuk) LIKE ?
                  AND stok > 0
                ORDER BY kategori, nama_barang
            """, (f"%{selected_motor}%",))
        else:
            cursor.execute("""
                SELECT nama_barang, stok, harga, kategori
                FROM barang
                WHERE stok > 0
                ORDER BY kategori, nama_barang
            """)

        data_barang = cursor.fetchall()

    if not data_barang:
        if selected_kategori and selected_motor:
            return f"Maaf, barang kategori {selected_kategori} untuk motor {selected_motor.capitalize()} belum tersedia saat ini."
        elif selected_kategori:
            return f"Maaf, barang kategori {selected_kategori} belum tersedia saat ini."
        elif selected_motor:
            return f"Maaf, sparepart untuk motor {selected_motor.capitalize()} belum tersedia saat ini."
        return "Barang tersedia tidak ditemukan."

    if selected_kategori and selected_motor:
        return (
            f"Barang kategori {selected_kategori} yang cocok untuk {selected_motor.capitalize()} "
            f"yang tersedia:<br>" + format_barang_table(data_barang, show_kategori=False)
        )
    elif selected_kategori:
        return (
            f"Barang kategori {selected_kategori} "
            f"yang tersedia:<br>" + format_barang_table(data_barang, show_kategori=False)
        )
    elif selected_motor:
        return (
            f"Barang yang cocok untuk {selected_motor.capitalize()} "
            f"yang tersedia:<br>" + format_barang_table(data_barang, show_kategori=True)
        )

    return (
        "Barang yang tersedia:<br>"
        + format_barang_table(data_barang, show_kategori=True)
    )

# =====================================
# DIAGNOSA MOTOR
# =====================================
def handle_diagnosa(user_input):
    text = user_input.lower()
    words = set(re.findall(r'[a-zA-Z0-9]+', text))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT kata_kunci, solusi_analisis FROM diagnosa_keluhan")
        data_diagnosa = cursor.fetchall()

    matches = []
    for row in data_diagnosa:
        kw = row['kata_kunci']
        solusi = row['solusi_analisis']
        parts = kw.split()

        if all(part in words for part in parts):
            matches.append((kw, solusi))

    if not matches:
        return "Silakan jelaskan keluhan motor secara lebih detail."

    matches = sorted(matches, key=lambda x: len(x[0]), reverse=True)

    kw = matches[0][0]
    solusi = matches[0][1]

    if kw == 'brebet':
        match_cond = re.search(r'\b(pas|saat|ketika|kalau|pada|waktu)\s+([a-zA-Z0-9\s]+)', text)
        if match_cond:
            kondisi = match_cond.group(2).strip()
            solusi = solusi.replace("Motor brebet dapat", f"Motor brebet saat {kondisi} dapat")

    return solusi

def is_known_diagnosa(text):
    text = text.lower()
    words = set(re.findall(r'[a-zA-Z0-9]+', text))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT kata_kunci FROM diagnosa_keluhan")
        keywords = [row[0] for row in cursor.fetchall() if row[0]]

    for kw in keywords:
        parts = kw.split()
        if all(part in words for part in parts):
            return True

    return False

# =====================================
# REKOMENDASI PRODUK
# =====================================
def handle_rekomendasi_produk(user_input):
    text = user_input.lower()
    words = set(re.findall(r'[a-zA-Z0-9]+', text))

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT LOWER(kategori) FROM barang")
        db_categories = [row[0] for row in cursor.fetchall() if row[0]]

        cursor.execute("SELECT DISTINCT LOWER(cocok_untuk) FROM barang")
        db_motors = set()
        for row in cursor.fetchall():
            if row[0]:
                for m in row[0].split(','):
                    motor_name = m.strip()
                    if motor_name:
                        db_motors.add(motor_name)

    sorted_categories = sorted(db_categories, key=len, reverse=True)
    detected_kategori = None
    for kat in sorted_categories:
        kat_lower = kat.lower()
        if ' ' in kat_lower:
            if kat_lower in text:
                detected_kategori = kat
                break
        else:
            if kat_lower in words:
                detected_kategori = kat
                break

    if not detected_kategori:
        for kat in sorted_categories:
            kat_words = [w for w in kat.split() if len(w) > 3]
            if kat_words and any(w in words for w in kat_words):
                detected_kategori = kat
                break

    sorted_motors = sorted(list(db_motors), key=len, reverse=True)
    detected_motor = None
    for motor in sorted_motors:
        if motor in words:
            detected_motor = motor
            break

    with get_db_connection() as conn:
        cursor = conn.cursor()

        if detected_kategori and detected_motor:
            cursor.execute("""
                SELECT nama_barang, harga, stok
                FROM barang
                WHERE LOWER(kategori) = ?
                  AND LOWER(cocok_untuk) LIKE ?
                  AND stok > 0
            """, (detected_kategori, f"%{detected_motor}%"))
            results = cursor.fetchall()

            if not results:
                return f"Maaf, rekomendasi {detected_kategori} yang cocok untuk motor {detected_motor.capitalize()} belum tersedia saat ini."

            return f"Rekomendasi {detected_kategori} yang cocok untuk {detected_motor.capitalize()}:<br>" + format_barang_table(results, show_kategori=False, show_price_stock=True)

        elif detected_kategori:
            cursor.execute("""
                SELECT nama_barang, harga, stok, cocok_untuk
                FROM barang
                WHERE LOWER(kategori) = ?
                  AND stok > 0
            """, (detected_kategori,))
            results = cursor.fetchall()

            if not results:
                return f"Maaf, stok barang untuk kategori {detected_kategori} belum tersedia saat ini."

            return f"Berikut rekomendasi produk kategori {detected_kategori.capitalize()} yang tersedia:<br>" + format_barang_table(results, show_kategori=False, show_price_stock=True)

        elif detected_motor:
            cursor.execute("""
                SELECT nama_barang, kategori, harga, stok
                FROM barang
                WHERE LOWER(cocok_untuk) LIKE ?
                  AND stok > 0
            """, (f"%{detected_motor}%",))
            results = cursor.fetchall()

            if not results:
                return f"Maaf, rekomendasi sparepart untuk motor {detected_motor.capitalize()} belum tersedia saat ini."

            return f"Berikut beberapa sparepart yang cocok untuk {detected_motor.capitalize()}:<br>" + format_barang_table(results, show_kategori=True, show_price_stock=True)

        else:
            return "Silakan sebutkan tipe motor (seperti Beat, Vario, Mio) or jenis sparepart (seperti Oli, Ban, Aki) yang Anda cari untuk mendapatkan rekomendasi."

# =====================================
# PENCOCOKAN BARANG
# =====================================
def score_barang_match(text, nama_barang, kategori):
    text_words = set(
        re.findall(
            r'[a-zA-Z0-9]+',
            text.lower()
        )
    )

    nama_words = set(
        re.findall(
            r'[a-zA-Z0-9]+',
            nama_barang.lower()
        )
    )

    kategori_words = set(
        re.findall(
            r'[a-zA-Z0-9]+',
            kategori.lower()
        )
    )

    user_parts = text_words.intersection(PART_KEYWORDS)
    if user_parts:
        candidate_words = nama_words.union(kategori_words)
        if not candidate_words.intersection(user_parts):
            return 0

    # Verifikasi Brand/Tipe Deskriptor untuk menghindari pencocokan salah (False Positive)
    user_descriptors = get_user_descriptors(text)
    if user_descriptors:
        candidate_words = nama_words.union(kategori_words)
        if not user_descriptors.intersection(candidate_words):
            return 0

    nama_score = len(text_words.intersection(nama_words))
    kategori_score = len(text_words.intersection(kategori_words))

    return nama_score * 2 + kategori_score

def find_best_barang(text, data_barang):
    best_barang = None
    best_score = 0

    for barang in data_barang:
        score = score_barang_match(
            text,
            barang[0],
            barang[1]
        )

        if score > best_score:
            best_barang = barang
            best_score = score

    if best_score == 0:
        return None

    return best_barang

# =====================================
# CEK STOK BARANG
# =====================================
def handle_check_stock(user_input):
    text = user_input.lower()

    # Cek jika kueri bersifat umum (tanpa brand)
    part_name = get_user_part_keyword(text)
    if part_name:
        user_descriptors = get_user_descriptors(text)
        if not user_descriptors:
            # Alihkan ke rekomendasi produk kategori
            recommendation = handle_rekomendasi_produk(user_input)
            if "rekomendasi" in recommendation.lower() or "beberapa sparepart" in recommendation.lower():
                return recommendation

    with get_db_connection() as conn:
        cursor = conn.conn.cursor() if hasattr(conn, 'conn') else conn.cursor()
        cursor.execute("""
            SELECT nama_barang, kategori, stok
            FROM barang
        """)
        data_barang = cursor.fetchall()

    barang = find_best_barang(
        text,
        data_barang
    )

    if barang:
        stok = barang[2]
        return f"Ya! Kami menyediakan {barang[0]}. Stok saat ini tersedia sebanyak {stok} pcs."

    # Jika tidak ditemukan di database
    if part_name:
        if part_name in TIDAK_DISEDIAKAN_PARTS:
            return f"Mohon maaf, bengkel kami saat ini belum menyediakan produk {part_name}. Kami hanya menyediakan suku cadang standar dan layanan servis motor Kurnia."
        else:
            return f"Mohon maaf, produk {part_name} tersebut saat ini belum tersedia di database kami. Silakan ketik 'daftar barang' untuk melihat suku cadang yang ready."

    return "Barang yang dicari tidak ditemukan. Silakan ketik 'daftar barang' untuk melihat stok tersedia."

# =====================================
# INFO BARANG
# =====================================
def handle_info_barang(user_input):
    text = user_input.lower()

    # Cek jika kueri bersifat umum (tanpa brand)
    part_name = get_user_part_keyword(text)
    if part_name:
        user_descriptors = get_user_descriptors(text)
        if not user_descriptors:
            # Alihkan ke rekomendasi produk kategori
            recommendation = handle_rekomendasi_produk(user_input)
            if "rekomendasi" in recommendation.lower() or "beberapa sparepart" in recommendation.lower():
                return recommendation

    with get_db_connection() as conn:
        cursor = conn.conn.cursor() if hasattr(conn, 'conn') else conn.cursor()
        cursor.execute("""
            SELECT nama_barang, kategori, harga, stok
            FROM barang
        """)
        data_barang = cursor.fetchall()

    barang = find_best_barang(
        text,
        data_barang
    )

    if barang:
        harga = barang[2]
        stok = barang[3]
        return f"Ya! {barang[0]} tersedia di bengkel kami dengan harga Rp{harga} dan stok {stok} pcs."

    # Jika tidak ditemukan di database
    if part_name:
        if part_name in TIDAK_DISEDIAKAN_PARTS:
            return f"Mohon maaf, bengkel kami saat ini belum menyediakan produk {part_name}."
        else:
            return f"Mohon maaf, informasi untuk produk {part_name} tersebut saat ini belum tersedia di database kami."

    return "Informasi barang tidak ditemukan. Coba gunakan nama produk or kategori yang lebih spesifik."
