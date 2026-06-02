import pandas as pd
import os
import re
import joblib
import sqlite3

from sklearn.metrics.pairwise import cosine_similarity

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# =========================
# PATH
# =========================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    'data',
    'processed',
    'dataset_clean.csv'
)

DB_PATH = os.path.join(
    BASE_DIR,
    'database',
    'chatbot.db'
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    'models',
    'tfidf_vectorizer.pkl'
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    'models',
    'naive_bayes_model.pkl'
)

LABEL_PATH = os.path.join(
    BASE_DIR,
    'models',
    'label_encoder.pkl'
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    DATA_PATH,
    keep_default_na=False
)

df['processed_question'] = df[
    'processed_question'
].fillna('').astype(str).str.strip()

vectorizer = joblib.load(VECTORIZER_PATH)

model = joblib.load(MODEL_PATH)

label_encoder = joblib.load(LABEL_PATH)

# =========================
# STEMMER & STOPWORD
# =========================
stemmer = StemmerFactory().create_stemmer()

stopwords = StopWordRemoverFactory().get_stop_words()

# =========================
# KEYWORD DOMAIN BENGKEL
# =========================
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
    "barang",
    "produk",
    "daftar",
    "jenis",
    "pilihan"
]

# =========================
# PREPROCESSING
# =========================
def preprocess_text(text):

    text = str(text).lower()

    text = re.sub(r'[^a-zA-Z\s]', '', text)

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

# =========================
# DETEKSI DOMAIN BENGKEL
# =========================
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

# =========================
# RESPONSE FALLBACK
# =========================
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

# =========================
# DAFTAR BARANG TERSEDIA
# =========================
def handle_list_barang(user_input):

    text = user_input.lower()

    conn = sqlite3.connect(DB_PATH)

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

    conn.close()

    if not data_barang:

        return "Barang tersedia tidak ditemukan."

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

# =========================
# CHATBOT LOOP
# =========================
print("=== CHATBOT BENGKEL ===")
print("Ketik pertanyaan Anda")
print("Ketik 'makasih' atau 'cukup' untuk keluar")
print()

while True:

    # =========================
    # INPUT USER
    # =========================
    user_input = input("Anda: ")

    # =========================
    # PREPROCESSING
    # =========================
    processed_input = preprocess_text(
        user_input
    )

    # =========================
    # TF-IDF
    # =========================
    input_vector = vectorizer.transform(
        [processed_input]
    )

    # =========================
    # PREDIKSI INTENT
    # =========================
    prediction = model.predict(
        input_vector
    )

    predicted_intent = label_encoder.inverse_transform(
        prediction
    )[0]

    # =========================
    # CONFIDENCE
    # =========================
    probabilities = model.predict_proba(
        input_vector
    )

    confidence = probabilities.max()

    # =========================
    # FALLBACK LUAR DOMAIN
    # =========================
    if (
        confidence < 0.1
        or (
            not is_bengkel_domain(user_input)
            and predicted_intent not in [
                'sapaan',
                'akhir_percakapan',
                'bantuan_umum'
            ]
        )
    ):

        fallback_intent, response, action = get_fallback_response(
            user_input
        )

        print("Intent:", fallback_intent)
        print("Confidence:", confidence)
        print("\nChatbot:", response)

        if action == "open_wa":

            print(">> Trigger membuka WhatsApp")

        print()

        continue

    # =========================
    # DEBUG
    # =========================
    print("Intent:", predicted_intent)
    print("Confidence:", confidence)

    # =========================
    # FALLBACK
    # =========================
    if confidence < 0.1:

        print(
            "\nChatbot: Maaf, saya belum memahami pertanyaan Anda.\n"
        )

        continue

    # =========================
    # FILTER DATA BERDASARKAN INTENT
    # =========================
    filtered_data = df[
        df['intent'] == predicted_intent
    ]

    # =========================
    # VALIDASI DATA
    # =========================
    if filtered_data.empty:

        print(
            "\nChatbot: Data intent tidak ditemukan.\n"
        )

        continue

    # =========================
    # TF-IDF DALAM INTENT
    # =========================
    intent_vectors = vectorizer.transform(
        filtered_data['processed_question']
    )

    # =========================
    # COSINE SIMILARITY
    # =========================
    similarities = cosine_similarity(
        input_vector,
        intent_vectors
    )

    # =========================
    # AMBIL DATA TERBAIK
    # =========================
    best_match_index = similarities.argmax()

    best_match = filtered_data.iloc[
        best_match_index
    ]

    # =========================
    # RESPONSE
    # =========================
    response = best_match['jawaban']

    # =========================
    # ACTION
    # =========================
    action = best_match['action']

    if isinstance(action, str):

        action = action.strip().lower()

    if action == "list_barang":

        response = handle_list_barang(
            user_input
        )

    # =========================
    # OUTPUT CHATBOT
    # =========================
    print("\nChatbot:", response)

    # =========================
    # TRIGGER
    # =========================
    if action == "open_maps":

        print(">> Trigger membuka Google Maps")

    elif action == "open_wa":

        print(">> Trigger membuka WhatsApp")

    elif action == "diagnosa":

        print(">> Trigger analisis diagnosa motor")

    elif action == "check_stock":

        print(">> Trigger cek stok barang")

    elif action == "list_barang":

        print(">> Trigger menampilkan daftar barang")

    print()

    # =========================
    # AKHIR PERCAKAPAN
    # =========================
    if predicted_intent == "akhir_percakapan":

        print("=== Percakapan selesai ===")

        break
