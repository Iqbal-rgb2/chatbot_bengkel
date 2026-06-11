import os
import sys

# Add workspace root to sys.path to allow absolute imports like 'from web.config import ...'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from flask import Flask
from web.config import SECRET_KEY
from web.routes.chat import chat_bp
from web.routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

# =====================================================================
# BACKWARD COMPATIBILITY EXPORTS (For external tests & scripts)
# =====================================================================
from web.database import get_db_connection, simpan_riwayat_stok, simpan_log_chat
from web.nlp.preprocessor import (
    load_fuzzy_vocabulary, fuzzy_vocabulary, correct_word,
    normalize_user_input, preprocess_text
)
from web.nlp.classifier import (
    df, vectorizer, model, label_encoder,
    detect_bad_words, is_bengkel_domain, get_fallback_response,
    contains_any, prioritize_intent
)
from web.nlp.handlers import (
    format_barang_table, add_conversational_follow_up, check_conversational_context,
    handle_list_barang, handle_diagnosa, is_known_diagnosa,
    handle_rekomendasi_produk, score_barang_match, find_best_barang,
    handle_check_stock, handle_info_barang
)

if __name__ == '__main__':
    app.run(debug=True)
