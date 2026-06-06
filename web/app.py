from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    send_from_directory
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
# SECRET KEY (trigger reload: layanan keyword and autoscroll fixes)
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

THRESHOLD_NAIVE_BAYES = 0.15
THRESHOLD_COSINE_SIMILARITY = 0.35


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
    "bgst",
    "tolol",
    "goblok",
    "bego",
    "kontol",
    "memek",
    "peler",
    "pantek",
    "babi",
    "asu",
    "jancok",
    "jancuk",
    "bajingan",
    "brengsek",
    "sialan",
    "kampret",
    "keparat",
    "lonte",
    "perek",
    "jablay",
    "idiot"
]

# =====================================
# KEYWORD DOMAIN BENGKEL
# =====================================
domain_keywords = [
    "motor",
    "bengkel",
    "servis",
    "service",
    "layanan",
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
    "minggu",
    "sabtu",
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
    "switch",
    "alamat",
    "rute",
    "maps",
    "lokasi",
    "biaya",
    "ongkos",
    "tarif",
    "ngelitik",
    "goyang",
    "komstir",
    "stabil",
    "setang",
    "stang",
    "suspensi",
    "memantul",
    "keras",
    "drop",
    "tekor",
    "selip",
    "loyo",
    "gigi",
    "atas",
    "tinggi",
    "rpm",
    "bawah",
    "langsam",
    "blong",
    # Kata Kunci Bengkel Tambahan
    "piston",
    "seher",
    "klep",
    "noken",
    "shock",
    "shockbreaker",
    "karbu",
    "injektor",
    "pelek",
    "radiator",
    "coolant",
    "gasket",
    "paking",
    "kopling",
    "cakram",
    "kaliper",
    "tromol",
    "spidometer",
    "speedometer",
    "klakson",
    "dinamo",
    "koil",
    "spul",
    "kiprok",
    "ecu",
    "fuse",
    "cangklong",
    "accu",
    "sekring",
    "bongkar",
    "pasang",
    "ganti",
    "tambah",
    "kurang",
    "aus",
    "retak",
    "patah",
    "kendor",
    "kencang",
    "setel",
    "stel",
    "bersihkan",
    "perbaiki",
    "benerin",
    "rusak",
    "ngobos",
    "ngebul",
    "kasar",
    "halus",
    "oleng",
    "slip",
    "seret",
    "macet",
    "overheat",
    "tanjakan",
    "nanjak"
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
    "sedia": "tersedia",
    "nanjak": "tanjakan",
    # Singkatan Umum Baru
    "klo": "kalau",
    "kalo": "kalau",
    "tp": "tapi",
    "dgn": "dengan",
    "sy": "saya",
    "utk": "untuk",
    "blm": "belum",
    "belom": "belum",
    "bwt": "buat",
    "lg": "lagi",
    "tny": "tanya",
    "kpn": "kapan",
    # Singkatan Bengkel Baru
    "mtr": "motor",
    "bngkl": "bengkel",
    "bngk": "bengkel",
    "srvs": "servis",
    "serv": "servis",
    "sprprt": "sparepart",
    "spart": "sparepart",
    "rekom": "rekomendasi",
    "stk": "stok",
    "hrg": "harga",
    "almt": "alamat",
    "lks": "lokasi",
    "kntk": "kontak",
    "ol": "oli",
    "bs": "busi",
    "ak": "aki",
    "kmps": "kampas"
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

    blacklist_keywords = [
        "sehat", "kesehatan", "dokter", "obat", "sakit", "klinik", "puskesmas", "rs", "medis",
        "makan", "makanan", "minum", "minuman", "lapar", "kenyang", "restoran", "cafe", "warung", "kuliner",
        "bank", "atm", "uang", "duit", "tabungan", "transfer", "kredit", "pinjaman", "finansial",
        "sekolah", "kuliah", "kampus", "dosen", "belajar", "siswa", "mahasiswa", "pelajaran",
        "politik", "pemilu", "pemerintah", "presiden", "menteri", "hukum",
        "pulsa", "internet", "wifi", "kuota", "game", "nonton", "film"
    ]

    for word in words:
        if word in blacklist_keywords:
            return False

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

    harga_servis_keywords = [
        "harga", "biaya", "ongkos", "tarif", "berapa", "bayar", "tarifnya"
    ]
    service_action_keywords = [
        "servis", "service", "tune", "up", "ganti", "perbaikan", "benerin", "perbaiki"
    ]

    if (
        contains_any(text_lower, harga_servis_keywords)
        and contains_any(text_lower, service_action_keywords)
    ):

        return "harga_servis"

    if contains_any(
        text_lower,
        [
            "layanan",
            "jasa",
            "servis",
            "service"
        ]
    ) and not contains_any(
        text_lower,
        product_keywords + ["harga", "biaya"]
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
# =====================================
# FORMAT HTML TABLE HELPER
# =====================================
def format_barang_table(results, show_kategori=False, show_price_stock=True):
    html = '<div class="chat-table-container"><table class="chat-table">'
    html += '<thead><tr>'
    html += '<th style="text-align: left;">Nama Barang</th>'
    
    # Check if 'kategori' exists in the results keys
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
    
    # 1. LAYANAN SERVIS (DIAGNOSA KELUHAN)
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
            
    # 2. REKOMENDASI PRODUK & DAFTAR BARANG
    elif intent in ["rekom_produk", "daftar_barang"]:
        # Coba deteksi motor
        motor = None
        for m in ["beat", "vario", "mio", "nmax", "scoopy", "pcx", "supra"]:
            if m in text:
                motor = m.capitalize()
                break
        
        # Coba deteksi kategori
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

    # 3. CEK STOK & INFO BARANG
    elif intent in ["cek_stok", "info_barang"]:
        # Coba deteksi motor/barang
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

    # 4. LOKASI BENGKEL
    elif intent == "lokasi_bengkel":
        follow_up_text = "<br><br>Apakah Anda ingin mengetahui jam buka/tutup operasional bengkel kami hari ini?"
        suggestions = ["Jam Buka Bengkel", "Hubungi WhatsApp", "Biaya Servis Motor"]

    # 5. JADWAL BENGKEL
    elif intent == "jadwal_bengkel":
        follow_up_text = "<br><br>Apakah Anda membutuhkan petunjuk arah atau link rute Google Maps untuk menuju ke bengkel kami?"
        suggestions = ["Alamat & Rute Maps", "Hubungi WhatsApp", "Lokasi Bengkel"]

    # 6. HARGA SERVIS
    elif intent == "harga_servis":
        follow_up_text = "<br><br>Apakah Anda ingin mengecek ketersediaan stok oli atau sparepart lainnya di bengkel kami?"
        suggestions = ["Cek Stok Oli", "Cek Stok Ban", "Jam Buka Bengkel"]

    # 7. SAPAAN & BANTUAN UMUM
    elif intent in ["sapaan", "bantuan_umum"]:
        follow_up_text = "<br><br>Anda bisa menanyakan lokasi, jam buka, stok sparepart, atau mendiagnosa keluhan motor."
        suggestions = ["Jam Buka Bengkel", "Lokasi Bengkel", "Motor saya brebet", "Oli untuk Vario"]

    # 8. FALLBACK & KATA KASAR
    else:
        suggestions = ["Jam Buka Bengkel", "Lokasi Bengkel", "Biaya Servis Motor", "Hubungi WhatsApp"]
        
    return response + follow_up_text, suggestions

# =====================================
# CONVERSATIONAL CONTEXT CHECKER
# =====================================
def check_conversational_context(user_input):
    text = user_input.strip().lower()
    
    # List kata konfirmasi bahasa Indonesia
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
    
    # List kata penolakan bahasa Indonesia
    reject_words = {
        "tidak", "nggak", "ngga", "ga", "gak", "no", "engga", "enggak", 
        "tidak usah", "ga usah", "g usah", "gosa", "gosaah", "no thanks",
        "nanti saja", "nanti", "belum", "g", "ndak", "nda", "ora", "ogah",
        "gamau", "ga mau", "nanti deh", "nanti aja", "nantiaja", "ntar",
        "ntar aja", "ntar saja", "tar aja", "skip", "cancel", "batal",
        "batalkan", "tidak perlu", "ga perlu", "ga usah deh", "g usah deh",
        "tidak usah deh", "gaperlu", "ndak usah", "nda usah"
    }
    
    # Jika input adalah konfirmasi dan ada suggestion sebelumnya
    if text in confirm_words:
        last_sug = session.get('last_suggestions')
        if last_sug and len(last_sug) > 0:
            # Ambil suggestion pertama sebagai target query
            target_query = last_sug[0]
            return target_query, None
            
    # Jika input adalah penolakan
    if any(rw in text for rw in reject_words) and len(text) <= 12:
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

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Ambil daftar kategori secara dinamis
        cursor.execute("SELECT nama_kategori FROM kategori_barang")
        kategori_barang = [row[0].lower() for row in cursor.fetchall() if row[0]]

        # Ambil daftar motor secara dinamis dari cocok_untuk
        cursor.execute("SELECT DISTINCT LOWER(cocok_untuk) FROM barang")
        db_motors = set()
        for row in cursor.fetchall():
            if row[0]:
                for m in row[0].split(','):
                    motor_name = m.strip()
                    if motor_name:
                        db_motors.add(motor_name)

    # Deteksi kategori yang dimaksud
    selected_kategori = None
    for kategori in kategori_barang:
        if kategori in text:
            selected_kategori = kategori
            break

    if not selected_kategori:
        for kategori in kategori_barang:
            words = [w for w in kategori.split() if len(w) > 3]
            if words and any(w in text for w in words):
                selected_kategori = kategori
                break

    # Deteksi motor yang dimaksud
    selected_motor = None
    sorted_motors = sorted(list(db_motors), key=len, reverse=True)
    for motor in sorted_motors:
        if motor in text:
            selected_motor = motor
            break

    # Lakukan query berdasarkan deteksi
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

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT kata_kunci, solusi_analisis FROM diagnosa_keluhan")
        data_diagnosa = cursor.fetchall()

    matches = []
    for row in data_diagnosa:
        kw = row['kata_kunci']
        solusi = row['solusi_analisis']
        parts = kw.split()

        if all(part in text for part in parts):
            matches.append((kw, solusi))

    if not matches:
        return "Silakan jelaskan keluhan motor secara lebih detail."

    # Urutkan berdasarkan panjang kata kunci terpanjang (jumlah kata/karakter)
    # agar pencarian lebih spesifik didahulukan
    matches = sorted(matches, key=lambda x: len(x[0]), reverse=True)

    kw = matches[0][0]
    solusi = matches[0][1]

    # Dinamisasi prefix untuk keluhan umum 'brebet' jika user memberikan kondisi spesifik
    if kw == 'brebet':
        match_cond = re.search(r'\b(pas|saat|ketika|kalau|pada|waktu)\s+([a-zA-Z0-9\s]+)', text)
        if match_cond:
            kondisi = match_cond.group(2).strip()
            solusi = solusi.replace("Motor brebet dapat", f"Motor brebet saat {kondisi} dapat")

    return solusi

def is_known_diagnosa(text):

    text = text.lower()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT kata_kunci FROM diagnosa_keluhan")
        keywords = [row[0] for row in cursor.fetchall() if row[0]]

    for kw in keywords:
        parts = kw.split()
        if all(part in text for part in parts):
            return True

    return False

# =====================================
# REKOMENDASI PRODUK
# =====================================
def handle_rekomendasi_produk(user_input):

    text = user_input.lower()

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Ambil daftar kategori secara dinamis
        cursor.execute("SELECT DISTINCT LOWER(kategori) FROM barang")
        db_categories = [row[0] for row in cursor.fetchall() if row[0]]

        # Ambil daftar motor secara dinamis dari cocok_untuk
        cursor.execute("SELECT DISTINCT LOWER(cocok_untuk) FROM barang")
        db_motors = set()
        for row in cursor.fetchall():
            if row[0]:
                for m in row[0].split(','):
                    motor_name = m.strip()
                    if motor_name:
                        db_motors.add(motor_name)

    # Urutkan berdasarkan panjang teks menurun agar pencocokan spesifik didahulukan
    sorted_categories = sorted(db_categories, key=len, reverse=True)
    detected_kategori = None
    for kat in sorted_categories:
        if kat in text:
            detected_kategori = kat
            break

    if not detected_kategori:
        for kat in sorted_categories:
            words = [w for w in kat.split() if len(w) > 3]
            if words and any(w in text for w in words):
                detected_kategori = kat
                break

    sorted_motors = sorted(list(db_motors), key=len, reverse=True)
    detected_motor = None
    for motor in sorted_motors:
        if motor in text:
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
            return "Silakan sebutkan tipe motor (seperti Beat, Vario, Mio) atau jenis sparepart (seperti Oli, Ban, Aki) yang Anda cari untuk mendapatkan rekomendasi."

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

    # List of known component/part keywords
    part_keywords = {
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

    user_parts = text_words.intersection(part_keywords)
    if user_parts:
        # Candidate item must match at least one of the user parts in its name or category
        candidate_words = nama_words.union(kategori_words)
        if not candidate_words.intersection(user_parts):
            return 0

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

# =====================================
# FAVICON
# =====================================
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

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
# PERFORMA & EVALUASI CHATBOT
# =====================================
@app.route('/performa')
def performa():

    if 'login' not in session:

        return redirect(
            url_for('login')
        )

    import json
    metrics_path = os.path.join(app.root_path, '..', 'data', 'processed', 'metrics.json')
    metrics = None
    
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
        except Exception as e:
            print(f"Error loading metrics.json: {e}")

    return render_template(
        'performa.html',
        metrics=metrics
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
# RESET CHAT SESSION
# =====================================
@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.pop('last_suggestions', None)
    return jsonify({'status': 'success', 'message': 'Chat session reset'})

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

            'confidence': 0,

            'suggestions': []

        })

    # =====================================
    # DETEKSI KATA KASAR
    # =====================================
    if detect_bad_words(user_input):
        response = "Mohon gunakan bahasa yang sopan dan santun ya. Silakan tanyakan kebutuhan motor Anda."
        response, suggestions = add_conversational_follow_up("bad_words", response, user_input)
        
        simpan_log_chat(
            user_input,
            user_input,
            "sarkasme_kasar",
            response
        )
        
        session['last_suggestions'] = suggestions
        return jsonify({
            'intent': 'sarkasme_kasar',
            'response': response,
            'action': None,
            'confidence': 1.0,
            'suggestions': suggestions
        })

    # =====================================
    # CONVERSATIONAL CONTEXT CHECKER (YES/NO CONFIRMATIONS)
    # =====================================
    target_query, direct_response = check_conversational_context(user_input)
    if direct_response:
        response, suggestions = direct_response
        simpan_log_chat(user_input, user_input, "konfirmasi_penolakan", response)
        session['last_suggestions'] = suggestions
        return jsonify({
            'intent': 'konfirmasi_penolakan',
            'response': response,
            'action': None,
            'confidence': 1.0,
            'suggestions': suggestions
        })
    elif target_query:
        user_input = target_query

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
        confidence < THRESHOLD_NAIVE_BAYES
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

        response, suggestions = add_conversational_follow_up(
            fallback_intent,
            response,
            normalized_input
        )

        simpan_log_chat(
            user_input,
            normalized_input,
            fallback_intent,
            response
        )

        session['last_suggestions'] = suggestions
        return jsonify({

            'intent': fallback_intent,

            'response': response,

            'action': action,

            'confidence': float(confidence),

            'suggestions': suggestions

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

    if best_similarity < THRESHOLD_COSINE_SIMILARITY:

        fallback_intent, response, action = get_fallback_response(
            normalized_input
        )

        response, suggestions = add_conversational_follow_up(
            fallback_intent,
            response,
            normalized_input
        )

        simpan_log_chat(
            user_input,
            normalized_input,
            fallback_intent,
            response
        )

        session['last_suggestions'] = suggestions
        return jsonify({

            'intent': fallback_intent,

            'response': response,

            'action': action,

            'confidence': float(confidence * best_similarity),

            'suggestions': suggestions

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

    response, suggestions = add_conversational_follow_up(
        predicted_intent,
        response,
        normalized_input
    )

    simpan_log_chat(
        user_input,
        normalized_input,
        predicted_intent,
        response
    )

    combined_confidence = float(confidence * best_similarity)

    session['last_suggestions'] = suggestions
    return jsonify({

        'intent': predicted_intent,

        'response': response,

        'action': action,

        'confidence': combined_confidence,

        'suggestions': suggestions

    })

# =====================================
# RUN APP
# =====================================
if __name__ == '__main__':

    app.run(
        debug=True
    )
