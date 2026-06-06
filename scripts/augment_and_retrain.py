import csv
import os
import random
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'dataset_clean.csv'
OUTPUT_PATH = BASE_DIR / 'data' / 'processed' / 'dataset_augmented.csv'
MODEL_PATH = BASE_DIR / 'models' / 'tfidf_vectorizer_augmented.pkl'
NB_MODEL_PATH = BASE_DIR / 'models' / 'naive_bayes_model_augmented.pkl'
LABEL_PATH = BASE_DIR / 'models' / 'label_encoder_augmented.pkl'

stemmer = StemmerFactory().create_stemmer()
stopwords = StopWordRemoverFactory().get_stop_words()


def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords]
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)


def expand_phrase_variants(phrases):
    variants = set()
    prefixes = [
        '', 'tolong ', 'apakah ', 'mohon ', 'kamu bisa ', 'saya ingin ',
        'bagaimana ', 'kira-kira ', 'apa ', 'ada ', 'dimana '
    ]
    suffixes = ['', ' dong', ' ya', ' sekarang', ' segera']

    for phrase in phrases:
        phrase = phrase.strip()
        phrase_clean = phrase.rstrip('?').strip()

        for prefix in prefixes:
            for suffix in suffixes:
                candidate = (prefix + phrase_clean + suffix).strip()
                if candidate:
                    variants.add(candidate)

        if 'servis' in phrase_clean:
            variants.add(phrase_clean.replace('servis', 'service'))
            variants.add('apakah ' + phrase_clean.replace('servis', 'service'))
        if 'service' in phrase_clean:
            variants.add(phrase_clean.replace('service', 'servis'))
        if 'whatsapp' in phrase_clean:
            variants.add(phrase_clean.replace('whatsapp', 'wa'))
        if 'wa' in phrase_clean and 'whatsapp' not in phrase_clean:
            variants.add(phrase_clean.replace('wa', 'whatsapp'))
        if 'di mana' in phrase_clean:
            variants.add(phrase_clean.replace('di mana', 'dimana'))
        if 'dimana' in phrase_clean:
            variants.add(phrase_clean.replace('dimana', 'di mana'))
        if 'bengkel' in phrase_clean and 'alamat' not in phrase_clean:
            variants.add('alamat bengkel ' + phrase_clean)

    return sorted(variants)


def make_templates():
    import json
    json_path = BASE_DIR / 'scripts' / 'seeder_data' / 'training_templates.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_augmentations(df, target_count=240):
    templates = make_templates()
    rows = []

    for intent, phrases in templates.items():
        intent_df = df[df['intent'] == intent].reset_index(drop=True)
        if intent_df.empty:
            continue

        # Fit a local vectorizer to match generated phrases to closest database questions
        from sklearn.feature_extraction.text import TfidfVectorizer
        local_vec = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')
        try:
            local_vec.fit(intent_df['processed_question'])
            db_vecs = local_vec.transform(intent_df['processed_question'])
            has_vocab = True
        except ValueError:
            has_vocab = False

        phrase_pool = expand_phrase_variants(phrases)

        for phrase in phrase_pool:
            if has_vocab:
                processed_phrase = preprocess_text(phrase)
                phrase_vec = local_vec.transform([processed_phrase])
                sims = cosine_similarity(phrase_vec, db_vecs)
                best_idx = sims.argmax()
                base_row = intent_df.iloc[best_idx].to_dict()
            else:
                base_row = intent_df.iloc[0].to_dict()

            rows.append({
                'intent': intent,
                'pertanyaan': phrase,
                'jawaban': base_row['jawaban'],
                'action': base_row['action'],
            })

    augmented = pd.DataFrame(rows)
    augmented['processed_question'] = augmented['pertanyaan'].apply(preprocess_text)
    augmented = augmented[~augmented['processed_question'].isin(df['processed_question'])]
    augmented = augmented.drop_duplicates(subset=['processed_question'])

    if len(augmented) < target_count:
        extra_rows = []
        existing_processed = set(augmented['processed_question']) | set(df['processed_question'])
        base_records = [r for r in rows]

        while len(augmented) + len(extra_rows) < target_count:
            record = random.choice(base_records)
            phrase = record['pertanyaan']
            intent = record['intent']
            jawaban = record['jawaban']
            action = record['action']

            candidate = random.choice([
                'tolong ', 'apakah ', 'mohon ', 'saya mau ', 'saya ingin ', 'bagaimana ', ''
            ]) + phrase
            candidate = candidate.strip()
            processed = preprocess_text(candidate)
            if processed and processed not in existing_processed:
                extra_rows.append({
                    'intent': intent,
                    'pertanyaan': candidate,
                    'jawaban': jawaban,
                    'action': action,
                    'processed_question': processed
                })
                existing_processed.add(processed)

        extra_df = pd.DataFrame(extra_rows)
        augmented = pd.concat([augmented, extra_df], ignore_index=True)

    augmented = augmented.sample(n=target_count, random_state=42).reset_index(drop=True)
    return augmented



def train_models(dataset):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(dataset['processed_question'])
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(dataset['intent'])
    model = MultinomialNB()
    model.fit(X, y)
    joblib.dump(vectorizer, MODEL_PATH)
    joblib.dump(model, NB_MODEL_PATH)
    joblib.dump(label_encoder, LABEL_PATH)
    return vectorizer, model, label_encoder


def load_models():
    vectorizer = joblib.load(MODEL_PATH)
    model = joblib.load(NB_MODEL_PATH)
    label_encoder = joblib.load(LABEL_PATH)
    return vectorizer, model, label_encoder


def is_bengkel_domain(text):
    keywords = [
        "motor", "bengkel", "servis", "service", "layanan", "oli", "busi", "aki", "ban",
        "rem", "mesin", "injeksi", "karburator", "sparepart", "stok", "kampas",
        "cvt", "rantai", "lampu", "starter", "brebet", "mogok", "mati", "hidup",
        "panas", "bunyi", "bocor", "gas", "tarikan", "tune", "up", "matic", "beat",
        "vario", "nmax", "scoopy", "pcx", "filter", "udara", "honda", "yamaha",
        "mio", "jadwal", "buka", "jam", "minggu", "sabtu", "kontak", "admin",
        "whatsapp", "nomor", "petugas", "chat", "produk", "barang", "rekomendasi",
        "cocok", "bagus", "terbaik", "knalpot", "bensin", "tektek", "asap", "putih",
        "percaya", "dipercaya", "murah", "velg", "spion", "cdi", "roller", "switch",
        "alamat", "rute", "maps", "lokasi", "biaya", "ongkos", "tarif", "ngelitik",
        "goyang", "komstir", "stabil", "setang", "stang", "suspensi", "memantul",
        "keras", "drop", "tekor", "selip", "loyo", "gigi", "atas", "tinggi", "rpm",
        "bawah", "langsam", "blong", "piston", "seher", "klep", "noken", "shock",
        "shockbreaker", "karbu", "injektor", "pelek", "radiator", "coolant",
        "gasket", "paking", "kopling", "cakram", "kaliper", "tromol", "spidometer",
        "speedometer", "klakson", "dinamo", "koil", "spul", "kiprok", "ecu",
        "fuse", "cangklong", "accu", "sekring", "bongkar", "pasang", "ganti",
        "tambah", "kurang", "aus", "retak", "patah", "kendor", "kencang", "setel",
        "stel", "bersihkan", "perbaiki", "benerin", "rusak", "ngobos", "ngebul",
        "kasar", "halus", "oleng", "slip", "seret", "macet", "overheat", "tanjakan",
        "nanjak"
    ]
    text = str(text).lower()
    words = re.findall(r'[a-zA-Z]+', text)
    
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
            
    return any(word in keywords for word in words)


def evaluate_model(vectorizer, model, label_encoder, dataset, test_questions):
    THRESHOLD_NAIVE_BAYES = 0.15
    THRESHOLD_COSINE_SIMILARITY = 0.30

    results = []
    for question in test_questions:
        processed = preprocess_text(question)
        x = vectorizer.transform([processed])
        pred = model.predict(x)[0]
        intent = label_encoder.inverse_transform([pred])[0]
        confidence = model.predict_proba(x).max()

        fallback = (confidence < THRESHOLD_NAIVE_BAYES)
        if not fallback:
            if intent not in ['sapaan', 'akhir_percakapan', 'bantuan_umum']:
                if not is_bengkel_domain(question):
                    fallback = True

        best_similarity = 0.0
        if not fallback:
            filtered_data = dataset[dataset['intent'] == intent]
            if not filtered_data.empty:
                intent_vectors = vectorizer.transform(filtered_data['processed_question'])
                similarities = cosine_similarity(x, intent_vectors)
                best_similarity = similarities.max()
                if best_similarity < THRESHOLD_COSINE_SIMILARITY:
                    fallback = True
            else:
                fallback = True

        if not fallback:
            combined_confidence = float(confidence * best_similarity)
        else:
            combined_confidence = float(confidence)

        results.append({
            'question': question,
            'predicted_intent': intent,
            'confidence': combined_confidence,
            'fallback': fallback
        })

    df_results = pd.DataFrame(results)
    metrics = {
        'total_questions': len(df_results),
        'fallback_count': int(df_results['fallback'].sum()),
        'fallback_rate': float(df_results['fallback'].mean()),
        'avg_confidence': float(df_results['confidence'].mean()),
        'avg_confidence_non_fallback': float(df_results.loc[~df_results['fallback'], 'confidence'].mean() if not df_results.loc[~df_results['fallback']].empty else 0.0),
        'intent_distribution': df_results['predicted_intent'].value_counts().to_dict()
    }
    return metrics, df_results


def make_synthetic_questions():
    base_questions = [
        'Apakah oli untuk vario tersedia?',
        'Bagaimana jadwal bengkel hari ini?',
        'Di mana alamat bengkel?',
        'Nomor WhatsApp bengkel berapa?',
        'Motor saya brebet ketika gas ditarik',
        'Ada stok aki untuk nmax?',
        'Berapa harga servis motor matic?',
        'Oli apa yang cocok untuk beat?',
        'Daftar oli yang tersedia dong',
        'Servis motor sampai jam berapa?',
        'Alamat bengkel senduro dimana?',
        'Bengkel buka hari minggu?',
        'Saya butuh rekomendasi oli',
        'Ada stok busi iridium?',
        'Bagaimana cara hubungi admin?',
        'Motor mati saat dijalankan',
        'Bisa bantu cek stok barang?',
        'Harga ganti oli berapa?',
        'Apa saja produk bengkel?',
        'Lokasi bengkel terdekat?',
        'Apakah bengkel buka sore?',
        'Cek stok filter udara',
        'Oli terbaik untuk honda saya',
        'Ganti ban motor berapa biayanya?',
        'Servis lengkap habis berapa?',
        'Ada stok kampas rem?',
        'Saran oli untuk scoopy',
        'Apa kelebihan oli yamalube?',
        'Bengkel buka jam berapa besok?',
        'Bagaimana cara ke bengkel?',
        'Chat admin bengkel',
        'Apakah bengkel melayani tune up?',
        'Stok aki motor ada?',
        'Service motor saya sekitar jam 3',
        'Daftar sparepart motor',
        'Ada produk motor matic?',
        'Apakah ada oli AHM?',
        'Motor tersendat saat jalan',
        'Bisa rekomendasi produk mesin?',
        'Dimana alamat bengkel?',
        'Apakah bengkel tutup jam 5?',
        'Saya ingin servis sore',
        'Minta nomor admin',
        'Oli mana yang cocok untuk PCX',
        'Daftar barang bengkel apa saja',
        'Motor bergetar saat digas',
        'Estimasi biaya servis motor',
        'Kapan bengkel buka?',
        'Di mana lokasi bengkel?',
        'Ada maps bengkel?',
        'Cek stok oli matic',
        'Servis motor biasa berapa biaya',
        'Motor susah hidup',
        'Apakah bengkel buka hari ini?',
        'Nomor telepon bengkel',
        'Apa saja fitur chatbot?',
        'Bisa bantu saya?',
        'Bagaimana cara ke bengkel dari jalan utama?',
        'Apakah stok oli tersedia?',
        'Saya perlu rekomendasi produk',
        'Motor saya mogok di jalan',
        'Bengkel buka sampai jam berapa?',
        'Apa jadwal bengkel?',
        'Daftar oli yang ready',
        'Ada oli shell atau yamalube?',
        'Info harga oli',
        'Motor tidak bisa distart',
        'Bisa cek stok ban?',
        'Hubungi petugas bengkel',
        'Mau servis motor besok',
        'Rekomendasi oli terbaik',
        'Lokasi bengkel sekitar sini',
        'Ada stok busi?',
        'Biaya ganti oli berapa?',
        'Apa saja sparepart tersedia?',
        'Bengkel ada dimana?',
        'Faq bengkel apa saja',
        'Apakah ada servis sore ini?',
        'Saya mau service motor',
        'Stok oli matic ready?',
        'Informasi oli yamalube',
        'Bagaimana menghubungi bengkel?',
        'Motor saya mendadak mati',
        'Daftar barang motor tersedia',
        'Apa rekomendasi oli untuk beat?',
        'Cek stok oli enduro',
        'Bengkel buka jam berapa sekarang?',
        'Saran produk untuk motor matik',
        'Motor berat saat gas',
        'Bisa saya dapatkan nomor wa?',
        'Lokasi bengkel Kurnia',
        'Harga servis apa saja?',
        'Daftar kategori barang',
        'Servis motor berapa lama?'
    ]
    if len(base_questions) >= 100:
        return base_questions[:100]
    extra = []
    while len(base_questions) + len(extra) < 100:
        extra.append(random.choice(base_questions))
    return base_questions + extra


def main():
    df = pd.read_csv(DATA_PATH, keep_default_na=False)
    augmented = generate_augmentations(df, target_count=240)
    combined = pd.concat([df, augmented], ignore_index=True)
    combined = combined.drop_duplicates(subset=['processed_question']).reset_index(drop=True)
    combined = combined.drop(columns=['id_chatbot'], errors='ignore')
    combined.insert(0, 'id_chatbot', range(1, len(combined) + 1))
    combined.to_csv(OUTPUT_PATH, index=False)
    print(f'Original dataset size: {len(df)} rows')
    print(f'Augmented dataset size: {len(combined)} rows')

    # ====================================================
    # METRIK EVALUASI ILMIAH (TRAIN-TEST SPLIT 80-20)
    # ====================================================
    print('\n=== Running Train-Test Split Evaluation (80-20) ===')
    
    # 1. Encode intent labels
    le_eval = LabelEncoder()
    combined['label'] = le_eval.fit_transform(combined['intent'])
    
    # 2. Split dataset with stratification to preserve class distribution
    train_df, test_df = train_test_split(
        combined,
        test_size=0.2,
        random_state=3,
        stratify=combined['label']
    )
    
    # 3. Fit Vectorizer and Classifier on training split
    vec_eval = TfidfVectorizer()
    X_train = vec_eval.fit_transform(train_df['processed_question'])
    y_train = train_df['label']
    
    clf_eval = MultinomialNB()
    clf_eval.fit(X_train, y_train)
    
    # 4. Predict on test split
    X_test = vec_eval.transform(test_df['processed_question'])
    y_test = test_df['label']
    y_pred = clf_eval.predict(X_test)
    
    # 5. Calculate metrics
    test_acc = accuracy_score(y_test, y_pred)
    print(f"Test Set Accuracy: {test_acc:.4f}")
    
    report_dict = classification_report(y_test, y_pred, target_names=le_eval.classes_, output_dict=True)
    
    # 6. Generate and Save Confusion Matrix Heatmap
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=le_eval.classes_,
        yticklabels=le_eval.classes_,
        cbar=True,
        square=True
    )
    plt.title('Confusion Matrix - Chatbot Intent Classification (80-20 Split)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Predicted Intent', fontsize=12, labelpad=10)
    plt.ylabel('True Intent', fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    
    models_cm_path = BASE_DIR / 'models' / 'confusion_matrix.png'
    web_cm_path = BASE_DIR / 'web' / 'static' / 'images' / 'confusion_matrix.png'
    
    # Ensure directories exist
    models_cm_path.parent.mkdir(parents=True, exist_ok=True)
    web_cm_path.parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(models_cm_path, dpi=300)
    plt.savefig(web_cm_path, dpi=300)
    plt.close()
    
    print(f"Confusion Matrix successfully saved to:")
    print(f"  - {models_cm_path}")
    print(f"  - {web_cm_path}")

    # 6.2. Generate and Save Classification Report Heatmap
    report_dict = classification_report(y_test, y_pred, target_names=le_eval.classes_, output_dict=True)
    df_report = pd.DataFrame(report_dict).transpose()
    
    # Drop 'support' since it is on a different scale (integer count vs 0.0-1.0 probabilities)
    df_metrics = df_report.drop(columns=['support'])
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df_metrics,
        annot=True,
        fmt='.4f',
        cmap='Blues',
        cbar=True,
        linewidths=0.5,
        linecolor='lightgrey'
    )
    plt.title('Classification Report Metrics - Chatbot Intent (80-20 Split)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Evaluation Metrics', fontsize=12, labelpad=10)
    plt.ylabel('Intent Classes / Averages', fontsize=12, labelpad=10)
    plt.tight_layout()
    
    models_rep_path = BASE_DIR / 'models' / 'classification_report.png'
    web_rep_path = BASE_DIR / 'web' / 'static' / 'images' / 'classification_report.png'
    
    plt.savefig(models_rep_path, dpi=300)
    plt.savefig(web_rep_path, dpi=300)
    plt.close()
    
    print(f"Classification Report image successfully saved to:")
    print(f"  - {models_rep_path}")
    print(f"  - {web_rep_path}")
    
    # 6.3. Save Metrics to metrics.json
    import json
    from datetime import datetime
    
    metrics_json_path = BASE_DIR / 'data' / 'processed' / 'metrics.json'
    metrics_data = {
        "accuracy": float(test_acc),
        "total_test_samples": int(len(y_test)),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "classification_report": report_dict
    }
    
    # Ensure directory exists
    metrics_json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics_data, f, indent=4)
        
    print(f"Metrics saved to JSON dashboard successfully at:\n  - {metrics_json_path}")
    
    # Clean up evaluation temporary label column
    combined = combined.drop(columns=['label'])
    
    # ====================================================
    # FINAL MODEL RETRAINING (100% DATA FOR PRODUCTION)
    # ====================================================
    print('\n=== Training Production Model (100% Data) ===')
    vectorizer, model, label_encoder = train_models(combined)
    print('Retraining complete. Production pickles updated.')

    test_questions = make_synthetic_questions()
    metrics, results = evaluate_model(vectorizer, model, label_encoder, combined, test_questions)
    print('\n=== Production Model Evaluation on 100 synthetic questions ===')
    print(f"Total questions: {metrics['total_questions']}")
    print(f"Fallback count: {metrics['fallback_count']}")
    print(f"Fallback rate: {metrics['fallback_rate']:.2%}")
    print(f"Average confidence: {metrics['avg_confidence']:.3f}")
    print(f"Average confidence (non-fallback): {metrics['avg_confidence_non_fallback']:.3f}")
    print('\nIntent distribution:')
    for intent, count in sorted(metrics['intent_distribution'].items(), key=lambda x: -x[1]):
        print(f'  {intent}: {count}')
    print('\nTop 10 low-confidence examples:')
    low_confidence = results.sort_values('confidence').head(10)
    for _, row in low_confidence.iterrows():
        print(f"  {row['question']} -> {row['predicted_intent']} (conf={row['confidence']:.3f}, fallback={row['fallback']})")


if __name__ == '__main__':
    main()
