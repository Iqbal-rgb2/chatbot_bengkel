from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

import pandas as pd
import sqlite3
import os
import re
import secrets
import joblib
from difflib import get_close_matches

from sklearn.metrics.pairwise import cosine_similarity

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from werkzeug.security import check_password_hash

app = Flask(__name__)

# =====================================
# SECRET KEY
# =====================================
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    secrets.token_hex(32)
)

# =====================================
# PATH
# =====================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    'data',
    'processed',
    'dataset_augmented.csv'
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    'models',
    'tfidf_vectorizer_augmented.pkl'
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    'models',
    'naive_bayes_model_augmented.pkl'
)

LABEL_PATH = os.path.join(
    BASE_DIR,
    'models',
    'label_encoder_augmented.pkl'
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    'database',
    'chatbot.db'
)


def get_db_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn

# =====================================
# LOAD DATA
# =====================================
df = pd.read_csv(DATA_PATH)

df = df.fillna('')

vectorizer = joblib.load(
    VECTORIZER_PATH
)

model = joblib.load(
    MODEL_PATH
)

label_encoder = joblib.load(
    LABEL_PATH
)

print("[OK] DATA LOADED :", df.shape)

print("[OK] INTENTS :")

print(df['intent'].unique())

# =====================================
# STEMMER & STOPWORD
# =====================================
stemmer = StemmerFactory().create_stemmer()

stopwords = StopWordRemoverFactory().get_stop_words()

# =====================================
# KATA KASAR
# =====================================
bad_words = [
    "anjing",
    "anjeng",
    "bangsat",
    "tolol",
    "goblok",
    "kontol",
    "memek"
]

# =====================================
# KEYWORD DOMAIN BENGKEL
# =====================================
domain_keywords = [
    "motor",
    "bengkel",
    "servis",
    "service",
    "oli",
    "busi",
    "aki",
    "ban",
    "rem",
    "mesin",
    "injeksi",
    "karburator",
    "sparepart",
    "stok",
    "kampas",
    "cvt",
    "rantai",
    "lampu",
    "starter",
    "brebet",
    "mogok",
    "mati",
    "hidup",
    "panas",
    "bunyi",
    "bocor",
    "gas",
    "tarikan",
    "tune",
    "up",
    "matic",
    "beat",
    "vario",
    "nmax",
    "scoopy",
    "pcx",
    "filter",
    "udara",
    "honda",
    "yamaha",
    "mio",
    "jadwal",
    "buka",
    "jam",
    "hari",
    "minggu",
    "sabtu",
    "pagi",
    "siang",
    "sore",
    "sekarang",
    "kontak",
    "admin",
    "whatsapp",
    "nomor",
    "petugas",
    "chat",
    "produk",
    "barang",
    "rekomendasi",
    "cocok",
    "bagus",
    "terbaik",
    "knalpot",
    "bensin",
    "tektek",
    "asap",
    "putih",
    "percaya",
    "dipercaya",
    "murah",
    "velg",
    "spion",
    "cdi",
    "roller",
    "switch"
]

# =====================================
# KAMUS SINGKATAN
# =====================================
abbreviation_words = {
    "brp": "berapa",
    "dmn": "dimana",
    "wa": "whatsapp",
    "no": "nomor",
    "nomer": "nomor",
    "yg": "yang",
    "gk": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "bntu": "bantu",
    "hlo": "halo",
    "helo": "halo",
    "asslmkm": "assalamualaikum",
    "brake": "rem",
    "sedia": "tersedia"
}

# =====================================
# VOCABULARY FUZZY
# =====================================
def load_fuzzy_vocabulary():

    vocabulary = set()

    for question in df['pertanyaan']:

        words = re.findall(
            r'[a-zA-Z]+',
            str(question).lower()
        )

        for word in words:

            if len(word) >= 4:

                vocabulary.add(word)

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT nama_barang,
               kategori
        FROM barang
    """)

        data_barang = cursor.fetchall()

    for barang in data_barang:

        for value in barang:

            words = re.findall(
                r'[a-zA-Z]+',
                str(value).lower()
            )

            for word in words:

                if len(word) >= 4:

                    vocabulary.add(word)

    cursor.execute("""
        SELECT nama_kategori
        FROM kategori_barang
    """)

    data_kategori = cursor.fetchall()

    for kategori in data_kategori:

        words = re.findall(
            r'[a-zA-Z]+',
            str(kategori[0]).lower()
        )

        for word in words:

            if len(word) >= 4:

                vocabulary.add(word)

    conn.close()

    return vocabulary

fuzzy_vocabulary = load_fuzzy_vocabulary()

# =====================================
# FUZZY CORRECTION
# =====================================
def correct_word(word):

    clean_word = word.lower()

    if clean_word in abbreviation_words:

        return abbreviation_words[clean_word]

    if len(clean_word) < 4:

        return clean_word

    if clean_word in fuzzy_vocabulary:

        return clean_word

    matches = get_close_matches(
        clean_word,
        fuzzy_vocabulary,
        n=1,
        cutoff=0.8
    )

    if matches:

        return matches[0]

    return clean_word

def normalize_user_input(text):

    words = re.findall(
        r'[a-zA-Z]+',
        str(text).lower()
    )

    normalized_words = [
        correct_word(word)
        for word in words
    ]

    return ' '.join(
        normalized_words
    )

# =====================================
# PREPROCESSING
# =====================================
def preprocess_text(text):

    text = str(text).lower()

    text = re.sub(
        r'[^a-zA-Z\s]',
        '',
        text
    )

    tokens = text.split()

    tokens = [
        word for word in tokens
        if word not in stopwords
    ]

    tokens = [
        stemmer.stem(word)
        for word in tokens
    ]

    return ' '.join(tokens)

# =====================================
# DETEKSI KATA KASAR
# =====================================
def detect_bad_words(text):

    text = text.lower()

    for word in bad_words:

        if word in text:

            return True

    return False

# =====================================
# DETEKSI DOMAIN BENGKEL
# =====================================
def is_bengkel_domain(text):

    text = str(text).lower()

    words = re.findall(
        r'[a-zA-Z]+',
        text
    )

    for word in words:

        if word in domain_keywords:

            return True

    return False

# =====================================
# RESPONSE FALLBACK
# =====================================
def get_fallback_response(text):

    if is_bengkel_domain(text):

        return (
            'fallback_bengkel',
            (
                'Pertanyaan Anda masih berkaitan '
                'dengan bengkel motor, tetapi '
                'informasi tersebut belum tersedia '
                'di database chatbot. Silakan '
                'hubungi petugas untuk bantuan '
                'lebih lanjut.'
            ),
            'open_wa'
        )

    return (
        'fallback_luar_bengkel',
        (
            'Maaf, saya hanya dapat membantu '
            'pertanyaan seputar bengkel motor, '
            'seperti jadwal, lokasi, servis, '
            'stok barang, dan rekomendasi '
            'produk.'
        ),
        None
    )

# =====================================
# PRIORITAS INTENT BERDASARKAN KEYWORD
# =====================================
def contains_any(text, keywords):

    words = set(
        re.findall(
            r'[a-zA-Z]+',
            str(text).lower()
        )
    )

    return any(
        keyword in words
        for keyword in keywords
    )

def prioritize_intent(text, predicted_intent):

    text_lower = str(text).lower()

    if (
        predicted_intent == "sapaan"
        and contains_any(
            text_lower,
            [
                "halo",
                "hai",
                "hallo",
                "selamat",
                "salam",
                "assalamualaikum",
                "permisi",
                "punten"
            ]
        )
        and not contains_any(
            text_lower,
            [
                "admin"
            ]
        )
    ):

        return predicted_intent

    product_keywords = [
        "barang",
        "produk",
        "sparepart",
        "oli",
        "busi",
        "aki",
        "ban",
        "kampas",
        "rem",
        "cakram",
        "filter",
        "udara",
        "lampu",
        "velg",
        "knalpot",
        "karburator",
        "cdi",
        "spion",
        "roller",
        "switch",
        "starter",
        "honda",
        "yamaha",
        "mio",
        "beat",
        "vario",
        "nmax",
        "pcx",
        "scoopy"
    ]

    if contains_any(
        text_lower,
        [
            "halo",
            "hai",
            "hallo",
            "salam",
            "assalamualaikum",
            "permisi",
            "punten"
        ]
    ) and not contains_any(
        text_lower,
        [
            "admin"
        ]
    ):

        return "sapaan"

    if contains_any(
        text_lower,
        [
            "percaya",
            "dipercaya",
            "terpercaya",
            "murah"
        ]
    ) and contains_any(
        text_lower,
        [
            "bengkel"
        ]
    ):

        return "bantuan_umum"

    if contains_any(
        text_lower,
        [
            "mogok",
            "brebet",
            "rem",
            "mesin",
            "bensin",
            "asap",
            "bunyi",
            "tektek"
        ]
    ) and not contains_any(
        text_lower,
        [
            "harga",
            "biaya"
        ]
    ):

        return "layanan_servis"

    if (
        contains_any(
            text_lower,
            [
                "daftar",
                "list",
                "jenis",
                "pilihan"
            ]
        )
        or "ada apa saja" in text_lower
        or "apa saja" in text_lower
    ) and contains_any(
        text_lower,
        product_keywords
    ):

        return "daftar_barang"

    if contains_any(
        text_lower,
        [
            "kontak",
            "admin",
            "whatsapp",
            "nomor",
            "petugas",
            "hubungi",
            "chat"
        ]
    ):

        return "kontak_admin"

    if contains_any(
        text_lower,
        [
            "jadwal",
            "buka",
            "jam",
            "hari",
            "minggu",
            "sabtu",
            "sore",
            "sekarang"
        ]
    ):

        return "jadwal_bengkel"

    if (
        contains_any(
            text_lower,
            [
                "rekomendasi",
                "cocok",
                "bagus",
                "terbaik"
            ]
        )
        or (
            "oli untuk" in text_lower
            and contains_any(
                text_lower,
                product_keywords
            )
        )
    ):

        return "rekom_produk"

    if (
        contains_any(
            text_lower,
            [
                "stok",
                "tersedia",
                "ada",
                "sedia",
                "cek"
            ]
        )
        and contains_any(
            text_lower,
            product_keywords
        )
    ):

        return "cek_stok"

    if (
        contains_any(
            text_lower,
            [
                "informasi",
                "info",
                "harga"
            ]
        )
        and contains_any(
            text_lower,
            product_keywords
        )
    ):

        return "info_barang"

    return predicted_intent

# =====================================
# DAFTAR BARANG TERSEDIA
# =====================================
def handle_list_barang(user_input):

    text = user_input.lower()

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nama_kategori
            FROM kategori_barang
        """)

        kategori_barang = [
            row[0].lower()
            for row in cursor.fetchall()
        ]

        selected_kategori = None

        for kategori in kategori_barang:

            if kategori in text:

                selected_kategori = kategori

                break

        if selected_kategori:

            cursor.execute(
                """
                SELECT nama_barang,
                       stok,
                       harga
                FROM barang
                WHERE LOWER(kategori) = ?
                  AND stok > 0
                ORDER BY nama_barang
                """,
                (selected_kategori,)
            )

        else:

            cursor.execute("""
                SELECT nama_barang,
                       stok,
                       harga
                FROM barang
                WHERE stok > 0
                ORDER BY kategori,
                         nama_barang
            """)

        data_barang = cursor.fetchall()

    if not data_barang:

        if selected_kategori:

            return (
                f"Barang kategori {selected_kategori} "
                "belum tersedia di stok bengkel."
            )

        return (
            "Barang tersedia tidak ditemukan."
        )

    daftar_barang = [
        f"{nama} ({stok} pcs, Rp{harga})"
        for nama, stok, harga in data_barang
    ]

    if selected_kategori:

        return (
            f"Barang kategori {selected_kategori} "
            f"yang tersedia: "
            + "; ".join(daftar_barang)
            + "."
        )

    return (
        "Barang yang tersedia: "
        + "; ".join(daftar_barang)
        + "."
    )

# =====================================
# DIAGNOSA MOTOR
# =====================================
def handle_diagnosa(user_input):

    text = user_input.lower()

    if "brebet" in text:

        if "gas" in text:

            return (
                "Motor brebet saat digas biasanya "
                "disebabkan karburator atau "
                "injektor kotor."
            )

        elif "tanjakan" in text:

            return (
                "Motor brebet saat tanjakan "
                "biasanya karena suplai bahan "
                "bakar kurang optimal atau "
                "CVT mulai lemah."
            )

        elif "dingin" in text:

            return (
                "Motor brebet saat kondisi "
                "dingin biasanya karena "
                "busi atau setting udara "
                "belum optimal."
            )

        return (
            "Motor brebet dapat disebabkan "
            "oleh busi, karburator, injektor, "
            "atau filter udara."
        )

    if "mogok" in text:

        return (
            "Motor mogok bisa disebabkan aki lemah, "
            "busi bermasalah, suplai bensin tidak lancar, "
            "atau sistem pengapian terganggu."
        )

    if "rem" in text:

        return (
            "Masalah rem bisa disebabkan kampas rem aus, "
            "setelan rem kurang tepat, atau komponen rem "
            "perlu dibersihkan."
        )

    if "asap" in text:

        return (
            "Asap putih dari motor biasanya berkaitan "
            "dengan oli yang ikut terbakar atau kondisi "
            "mesin yang perlu diperiksa."
        )

    if "bensin" in text:

        return (
            "Jika motor kehabisan bensin, isi bahan bakar "
            "terlebih dahulu lalu coba starter ulang. Jika "
            "tetap bermasalah, sistem bahan bakar perlu dicek."
        )

    if "bunyi" in text:

        return (
            "Bunyi tidak normal pada motor bisa berasal dari "
            "rantai, CVT, rem, atau bagian mesin. Sebaiknya "
            "dicek langsung agar sumber bunyinya jelas."
        )

    return (
        "Silakan jelaskan keluhan motor "
        "secara lebih detail."
    )

def is_known_diagnosa(text):

    text = text.lower()

    diagnosa_keywords = [
        "brebet",
        "mogok",
        "rem",
        "bunyi",
        "asap",
        "bensin",
        "susah hidup",
        "rem keras",
        "mesin cepat panas",
        "mesin panas"
    ]

    for keyword in diagnosa_keywords:

        if keyword in text:

            return True

    return False

# =====================================
# REKOMENDASI PRODUK
# =====================================
def handle_rekomendasi_produk(user_input):

    text = user_input.lower()

    if "oli" in text:

        if "beat" in text:

            return (
                "Oli yang cocok untuk Honda "
                "Beat adalah AHM MPX 2 "
                "atau Motul Scooter Expert."
            )

        elif "vario" in text:

            return (
                "Oli yang cocok untuk Honda "
                "Vario adalah AHM MPX 2 "
                "atau Yamalube Super Matic."
            )

    return (
        "Silakan sebutkan jenis motor "
        "atau produk yang ingin dicari."
    )

# =====================================
# PENCOCOKAN BARANG
# =====================================
def score_barang_match(text, nama_barang, kategori):

    text_words = set(
        re.findall(
            r'[a-zA-Z]+',
            text.lower()
        )
    )

    nama_words = set(
        re.findall(
            r'[a-zA-Z]+',
            nama_barang.lower()
        )
    )

    kategori_words = set(
        re.findall(
            r'[a-zA-Z]+',
            kategori.lower()
        )
    )

    nama_score = len(
        text_words.intersection(nama_words)
    )

    kategori_score = len(
        text_words.intersection(kategori_words)
    )

    return (
        nama_score * 2
        + kategori_score
    )

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

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT nama_barang,
                   kategori,
                   stok
            FROM barang
        """)

        data_barang = cursor.fetchall()

    barang = find_best_barang(
        text,
        data_barang
    )

    if barang:

        stok = barang[2]

        return (
            f"Stok {barang[0]} tersedia "
            f"sebanyak {stok} pcs."
        )

    return (
        "Barang yang dicari tidak ditemukan. "
        "Silakan ketik 'daftar barang' untuk melihat stok tersedia."
    )

# =====================================
# INFO BARANG
# =====================================
def handle_info_barang(user_input):

    text = user_input.lower()

    with get_db_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT nama_barang,
                   kategori,
                   harga,
                   stok
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

        return (
            f"{barang[0]} memiliki harga "
            f"Rp{harga} dengan stok "
            f"tersedia {stok} pcs."
        )

    return (
        "Informasi barang tidak ditemukan. "
        "Coba gunakan nama produk atau kategori yang lebih spesifik."
    )

# =====================================
# SIMPAN RIWAYAT STOK
# =====================================
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

# =====================================
# SIMPAN LOG CHAT
# =====================================
def simpan_log_chat(
    pertanyaan,
    pertanyaan_normalisasi,
    intent,
    jawaban
):

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
            jawaban
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            pertanyaan,
            pertanyaan_normalisasi,
            intent,
            jawaban
        )
    )

    conn.commit()

    conn.close()

# =====================================
# HOME
# =====================================
@app.route('/')
def home():

    return render_template(
        'index.html'
    )

# =====================================
# LOGIN PETUGAS
# =====================================
@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    error = None

    if request.method == 'POST':

        username = request.form.get(
            'username'
        )

        password = request.form.get(
            'password'
        )

        conn = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id_admin,
                   password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        # =========================
        # LOGIN BERHASIL
        # =========================
        if (
            user
            and check_password_hash(
                user[1],
                password
            )
        ):

            session['login'] = True

            session['username'] = username

            session['id_admin'] = user[0]

            return redirect(
                url_for(
                    'dashboard_barang'
                )
            )

        # =========================
        # LOGIN GAGAL
        # =========================
        else:

            error = (
                "Username atau password salah."
            )

    return render_template(
        'login.html',
        error=error
    )

# =====================================
# DASHBOARD BARANG
# =====================================
@app.route('/dashboard_barang')
def dashboard_barang():

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_barang,
               nama_barang,
               kategori,
               harga,
               stok
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
@app.route('/riwayat_stok')
def riwayat_stok():

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

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
@app.route('/log_chat')
def log_chat():

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

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
# UPDATE KLASIFIKASI LOG CHAT
# =====================================
@app.route(
    '/update_klasifikasi_chat/<int:id>',
    methods=['POST']
)
def update_klasifikasi_chat(id):

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    klasifikasi = request.form.get(
        'klasifikasi'
    )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE log_chat
        SET klasifikasi = ?
        WHERE id_chat = ?
        """,
        (
            klasifikasi,
            id
        )
    )

    conn.commit()

    conn.close()

    return redirect(
        url_for('log_chat')
    )

# =====================================
# TAMBAH BARANG
# =====================================
@app.route(
    '/tambah_barang',
    methods=['POST']
)
def tambah_barang():

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    nama_barang = request.form.get(
        'nama_barang'
    )

    kategori = request.form.get(
        'kategori'
    )

    harga = request.form.get(
        'harga'
    )

    stok = request.form.get(
        'stok'
    )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO barang
        (
            nama_barang,
            kategori,
            harga,
            stok
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            nama_barang,
            kategori,
            harga,
            stok
        )
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

    return redirect(
        url_for('dashboard_barang')
    )

# =====================================
# EDIT BARANG
# =====================================
@app.route(
    '/edit_barang/<int:id>',
    methods=['POST']
)
def edit_barang(id):

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    nama_barang = request.form.get(
        'nama_barang'
    )

    kategori = request.form.get(
        'kategori'
    )

    harga = request.form.get(
        'harga'
    )

    stok = request.form.get(
        'stok'
    )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

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

    stok_lama = None

    if data_lama:

        stok_lama = data_lama[0]

    cursor.execute(
        """
        UPDATE barang
        SET
            nama_barang = ?,
            kategori = ?,
            harga = ?,
            stok = ?
        WHERE id_barang = ?
        """,
        (
            nama_barang,
            kategori,
            harga,
            stok,
            id
        )
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

    return redirect(
        url_for('dashboard_barang')
    )

# =====================================
# HAPUS BARANG
# =====================================
@app.route(
    '/hapus_barang/<int:id>'
)
def hapus_barang(id):

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

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

    stok_lama = None

    if data_lama:

        stok_lama = data_lama[0]

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

    return redirect(
        url_for('dashboard_barang')
    )

# =====================================
# LOGOUT
# =====================================
@app.route('/logout')
def logout():

    session.clear()

    return redirect(
        url_for('login')
    )

# =====================================
# CHAT API
# =====================================
@app.route(
    '/chat',
    methods=['POST']
)
def chat():

    user_input = request.json.get(
        'message',
        ''
    )

    if user_input.strip() == "":

        return jsonify({

            'intent': 'fallback',

            'response':
            'Silakan masukkan pertanyaan.',

            'action': None,

            'confidence': 0

        })

    # =====================================
    # DETEKSI KATA KASAR
    # =====================================
    warning_message = ""

    if detect_bad_words(user_input):

        warning_message = (
            "Mohon gunakan bahasa "
            "yang sopan &#128522;<br><br>"
        )

    # =====================================
    # PREPROCESSING
    # =====================================
    normalized_input = normalize_user_input(
        user_input
    )

    processed_input = preprocess_text(
        normalized_input
    )

    # =====================================
    # TF-IDF
    # =====================================
    input_vector = vectorizer.transform(
        [processed_input]
    )

    # =====================================
    # PREDIKSI INTENT
    # =====================================
    prediction = model.predict(
        input_vector
    )

    predicted_intent = label_encoder.inverse_transform(
        prediction
    )[0]

    # =====================================
    # PRIORITAS INTENT
    # =====================================
    predicted_intent = prioritize_intent(
        normalized_input,
        predicted_intent
    )

    # =====================================
    # CONFIDENCE
    # =====================================
    probabilities = model.predict_proba(
        input_vector
    )

    confidence = probabilities.max()

    # =====================================
    # FALLBACK
    # =====================================
    if (
        confidence < 0.1
        or (
            not is_bengkel_domain(normalized_input)
            and predicted_intent not in [
                'sapaan',
                'akhir_percakapan',
                'bantuan_umum'
            ]
        )
    ):

        fallback_intent, response, action = get_fallback_response(
            normalized_input
        )

        simpan_log_chat(
            user_input,
            normalized_input,
            fallback_intent,
            response
        )

        return jsonify({

            'intent': fallback_intent,

            'response': response,

            'action': action,

            'confidence': float(confidence)

        })

    # =====================================
    # FILTER INTENT
    # =====================================
    filtered_data = df[
        df['intent'] == predicted_intent
    ]

    # =====================================
    # BEST MATCH
    # =====================================
    intent_vectors = vectorizer.transform(

        filtered_data[
            'processed_question'
        ]

    )

    similarities = cosine_similarity(
        input_vector,
        intent_vectors
    )

    best_similarity = similarities.max()

    if best_similarity < 0.25:

        fallback_intent, response, action = get_fallback_response(
            normalized_input
        )

        simpan_log_chat(
            user_input,
            normalized_input,
            fallback_intent,
            response
        )

        return jsonify({

            'intent': fallback_intent,

            'response': response,

            'action': action,

            'confidence': float(confidence)

        })

    best_match_index = similarities.argmax()

    best_match = filtered_data.iloc[
        best_match_index
    ]

    response = best_match['jawaban']

    action = best_match.get(
        'action',
        None
    )

    if isinstance(action, str):

        action = action.strip().lower()

        if action == "":

            action = None

    # =====================================
    # ACTION LOGIC
    # =====================================
    if action == "diagnosa":

        if is_known_diagnosa(
            normalized_input
        ):

            response = handle_diagnosa(
                normalized_input
            )

        else:

            predicted_intent, response, action = get_fallback_response(
                normalized_input
            )

    elif action == "saran_produk":

        response = handle_rekomendasi_produk(
            normalized_input
        )

    elif action == "check_stock":

        response = handle_check_stock(
            normalized_input
        )

    elif action == "info_barang":

        response = handle_info_barang(
            normalized_input
        )

    elif action == "list_barang":

        response = handle_list_barang(
            normalized_input
        )

    response = warning_message + response

    simpan_log_chat(
        user_input,
        normalized_input,
        predicted_intent,
        response
    )

    return jsonify({

        'intent': predicted_intent,

        'response': response,

        'action': action,

        'confidence': float(confidence)

    })

# =====================================
# RUN APP
# =====================================
if __name__ == '__main__':

    app.run(
        debug=True
    )
