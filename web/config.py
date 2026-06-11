import os
import secrets

# =====================================
# PATH CONFIGURATIONS
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

# =====================================
# NLP THRESHOLDS
# =====================================
THRESHOLD_NAIVE_BAYES = 0.15
THRESHOLD_COSINE_SIMILARITY = 0.35

# =====================================
# FLASK SECRET KEY
# =====================================
SECRET_KEY = os.environ.get(
    "FLASK_SECRET_KEY",
    secrets.token_hex(32)
)
