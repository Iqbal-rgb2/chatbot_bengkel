import os
from flask import Blueprint, render_template, request, jsonify, session, send_from_directory, current_app
from sklearn.metrics.pairwise import cosine_similarity
from web.config import THRESHOLD_NAIVE_BAYES, THRESHOLD_COSINE_SIMILARITY
from web.database import simpan_log_chat
from web.nlp.preprocessor import normalize_user_input, preprocess_text
from web.nlp.classifier import (
    detect_bad_words, get_fallback_response, prioritize_intent, is_bengkel_domain,
    vectorizer, model, label_encoder, df
)
from web.nlp.handlers import (
    add_conversational_follow_up, check_conversational_context,
    handle_diagnosa, is_known_diagnosa, handle_rekomendasi_produk,
    handle_check_stock, handle_info_barang, handle_list_barang
)

chat_bp = Blueprint('chat', __name__)

# =====================================
# FAVICON
# =====================================
@chat_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# =====================================
# HOME
# =====================================
@chat_bp.route('/')
def home():
    return render_template(
        'index.html'
    )

# =====================================
# RESET CHAT SESSION
# =====================================
@chat_bp.route('/reset_session', methods=['POST'])
def reset_session():
    session.pop('last_suggestions', None)
    return jsonify({'status': 'success', 'message': 'Chat session reset'})

# =====================================
# CHAT API
# =====================================
@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get(
        'message',
        ''
    )

    if user_input.strip() == "":
        return jsonify({
            'intent': 'fallback',
            'response': 'Silakan masukkan pertanyaan.',
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
    # BEST MATCH (COSINE SIMILARITY)
    # =====================================
    intent_vectors = vectorizer.transform(
        filtered_data['processed_question']
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
