import pandas as pd
import os
import joblib

from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

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

# =========================
# LOAD TF-IDF
# =========================
vectorizer = joblib.load(
    VECTORIZER_PATH
)

# =========================
# TF-IDF TRANSFORM
# =========================
X = vectorizer.transform(
    df['processed_question']
)

# =========================
# ENCODE LABEL
# =========================
label_encoder = LabelEncoder()

y = label_encoder.fit_transform(
    df['intent']
)

# =========================
# TRAINING NAIVE BAYES
# =========================
model = MultinomialNB()

model.fit(X, y)

# =========================
# SIMPAN MODEL
# =========================
joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    label_encoder,
    LABEL_PATH
)

print("Training Naive Bayes berhasil!")

print(
    "Jumlah intent:",
    len(label_encoder.classes_)
)

print("Daftar intent:")

print(label_encoder.classes_)
