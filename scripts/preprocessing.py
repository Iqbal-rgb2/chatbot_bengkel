import pandas as pd
import re
import os
import sqlite3

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# =========================
# PATH PROJECT
# =========================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# =========================
# PATH DATABASE
# =========================
DB_PATH = os.path.join(
    BASE_DIR,
    'database',
    'chatbot.db'
)

# =========================
# KONEKSI SQLITE
# =========================
conn = sqlite3.connect(DB_PATH)

# =========================
# AMBIL DATA CHATBOT
# =========================
query = "SELECT * FROM chatbot_data"

df = pd.read_sql_query(query, conn)

# =========================
# HANDLE NULL
# =========================
df = df.fillna('')

# =========================
# DEBUG
# =========================
print("Kolom tabel:")
print(df.columns)

print("\nDaftar intent:")
print(df['intent'].unique())

print("\nJumlah data:")
print(len(df))

# =========================
# STEMMER
# =========================
stemmer_factory = StemmerFactory()

stemmer = stemmer_factory.create_stemmer()

# =========================
# STOPWORD
# =========================
stopword_factory = StopWordRemoverFactory()

stopwords = stopword_factory.get_stop_words()

# =========================
# PREPROCESSING
# =========================
def preprocess_text(text):

    # ubah ke lowercase
    text = str(text).lower()

    # hapus selain huruf
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # tokenizing
    tokens = text.split()

    # stopword removal
    tokens = [
        word for word in tokens
        if word not in stopwords
    ]

    # stemming
    tokens = [
        stemmer.stem(word)
        for word in tokens
    ]

    return ' '.join(tokens)

# =========================
# PREPROCESS KOLOM PERTANYAAN
# =========================
df['processed_question'] = df[
    'pertanyaan'
].apply(preprocess_text)

# =========================
# OUTPUT PATH
# =========================
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    'data',
    'processed',
    'dataset_clean.csv'
)

# =========================
# SIMPAN CSV
# =========================
df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nPreprocessing berhasil!")

# =========================
# TUTUP DATABASE
# =========================
conn.close()