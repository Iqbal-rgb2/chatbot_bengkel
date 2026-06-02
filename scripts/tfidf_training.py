import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer

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

MODEL_PATH = os.path.join(
    BASE_DIR,
    'models',
    'tfidf_vectorizer.pkl'
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

empty_questions = df['processed_question'].eq('')

if empty_questions.any():

    print(
        "Peringatan: ada",
        empty_questions.sum(),
        "baris processed_question kosong."
    )

if not df['processed_question'].ne('').any():

    raise ValueError(
        "Tidak ada processed_question yang berisi teks untuk TF-IDF."
    )

# =========================
# TF-IDF
# =========================
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(
    df['processed_question']
)

# =========================
# SIMPAN MODEL
# =========================
joblib.dump(
    vectorizer,
    MODEL_PATH
)

print("TF-IDF training berhasil!")

print(
    "Jumlah fitur:",
    len(vectorizer.get_feature_names_out())
)
