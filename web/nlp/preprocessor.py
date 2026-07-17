import re
import pandas as pd
from difflib import get_close_matches
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from web.config import DATA_PATH
from web.database import get_db_connection

# =====================================
# STEMMER & STOPWORD Sastrawi
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
    "dapatkah": "dapatkah",
    "bisakah": "bisakah",
    "sanggupkah": "sanggupkah",
    "melayani": "melayani",
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

    df = pd.read_csv(DATA_PATH)
    df = df.fillna('')

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
            SELECT nama_barang, kategori
            FROM barang
        """)
        data_barang = cursor.fetchall()

        cursor.execute("""
            SELECT nama_kategori
            FROM kategori_barang
        """)
        data_kategori = cursor.fetchall()

    for barang in data_barang:
        for value in barang:
            if value:
                words = re.findall(
                    r'[a-zA-Z]+',
                    str(value).lower()
                )
                for word in words:
                    if len(word) >= 4:
                        vocabulary.add(word)

    for kategori in data_kategori:
        if kategori[0]:
            words = re.findall(
                r'[a-zA-Z]+',
                str(kategori[0]).lower()
            )
            for word in words:
                if len(word) >= 4:
                    vocabulary.add(word)

    return vocabulary

# Inisialisasi kosakata fuzzy
fuzzy_vocabulary = load_fuzzy_vocabulary()

# =====================================
# FUZZY CORRECTION & NORMALIZATION
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

    return ' '.join(normalized_words)

# =====================================
# PREPROCESSING TEXT
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
