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
    templates = {
        'sapaan': [
            'halo', 'hai', 'hallo', 'selamat pagi', 'selamat siang', 'selamat sore',
            'permisi', 'assalamualaikum', 'salam', 'pagi bengkel', 'halo bengkel',
            'hei bengkel', 'hola bengkel', 'apa kabar bengkel', 'kabar baik',
            'ada yang bisa dibantu', 'hai admin', 'pagi', 'siang', 'malam',
            'halo semuanya', 'apa kabar', 'salam kenal', 'selamat datang',
            'halo semua', 'hallo semua', "assalamu'alaikum", "syalom", "salam sejahtera",
            "pagi min", "siang min", "sore min", "malam min", "halo kurnia", "hai kurnia",
            "hallo kurnia", "halo kak", "pagi kak", "siang kak", "sore kak", "malam kak",
            "halo petugas", "permisi petugas", "punten mang", "sampurasun", "spada",
            "permisi min", "oi", "oy"
        ],
        'bantuan_umum': [
            'tolong bantu saya', 'bantu saya', 'minta bantuan', 'saya perlu bantuan',
            'kamu bisa bantu apa', 'apa saja yang bisa dibantu', 'fitur chatbot apa',
            'apa layananmu', 'apa yang bisa kamu lakukan', 'informasi apa saja tersedia',
            'tunjukkan apa yang bisa ditanyakan', 'saya butuh informasi',
            'bantuan untuk bengkel', 'bantu jawab pertanyaan bengkel', 'chatbot ini bisa apa',
            'apakah kamu bisa bantu servis', 'apakah kamu bisa bantu stok',
            'apakah kamu bisa bantu lokasi', 'apa saja info bengkel', 'bisa bantu masalah motor',
            'bisa tolong', 'tolong infonya', 'tanya dong', 'tanya min', 'mau tanya min',
            'bisa nanya'
        ],
        'akhir_percakapan': [
            'terima kasih', 'makasih', 'matur nuwun', 'sudah cukup', 'cukup',
            'itu saja', 'sudah jelas', 'oke makasih', 'bye', 'sampai jumpa',
            'sudah membantu', 'terima kasih banyak', 'mantap terima kasih',
            'saya tutup', 'sampai ketemu lagi', 'thanks', 'selamat tinggal',
            'baik terima kasih', 'cukup ya', 'cukup terima kasih', 'udah cukup'
        ],
        'jadwal_bengkel': [
            'bengkel buka jam berapa', 'jam operasional bengkel', 'hari ini buka tidak',
            'buka sampai jam berapa', 'bengkel tutup jam berapa', 'hari minggu buka tidak',
            'sabtu buka tidak', 'bisa servis sore', 'jadwal bengkel gimana',
            'buka dari pagi jam berapa', 'bengkel libur hari apa', 'masih buka sekarang',
            'apa jam kerja bengkel', 'jam service bengkel', 'apakah bengkel buka hari ini',
            'bengkel tutup kapan', 'jam kerja bengkel hari ini', 'bengkel buka sampai sore',
            'apa hari ini bengkel buka', 'jadwal kerja bengkel'
        ],
        'lokasi_bengkel': [
            'alamat bengkel dimana', 'lokasi bengkel dimana', 'bengkel ada dimana',
            'share lokasi bengkel', 'ada maps bengkel', 'kirim alamat bengkel',
            'bengkel dekat mana', 'rute ke bengkel gimana', 'posisi bengkel dimana',
            'lokasi lengkap bengkel', 'maps kurnia motor', 'saya mau ke bengkel',
            'bagaimana menuju bengkel', 'bengkel terdekat di mana', 'lokasi bengkel terdekat',
            'di mana bengkel berada', 'alamat bengkel kurnia', 'bengkel motor kurnia dimana',
            'rute ke bengkel', 'petunjuk arah bengkel'
        ],
        'kontak_admin': [
            'nomor wa bengkel berapa', 'wa bengkel berapa', 'nomor whatsapp bengkel',
            'bisa hubungi lewat whatsapp', 'kontak admin ada', 'nomor telepon bengkel',
            'minta nomor admin', 'saya mau chat petugas', 'hubungi petugas bengkel',
            'nomor bengkel berapa', 'kontak bengkel', 'admin bisa dihubungi',
            'bagaimana hubungi bengkel', 'ada nomor admin', 'nomor kontak bengkel',
            'nomor cs bengkel', 'dapat nomor whatsapp bengkel', 'nomor hotline bengkel',
            'hubungi bengkel lewat whatsapp', 'chat admin bengkel'
        ],
        'cek_stok': [
            'stok oli yamalube matic', 'ada oli ahm mpx 2', 'oli enduro matic ready',
            'cek stok oli', 'ada stok aki motor', 'stok ban depan ada',
            'apakah ada kampas rem', 'stok busi iridium', 'cek stok sparepart',
            'apakah ada oli matic', 'ada stok oli motor', 'stok bagian motor ada',
            'cek stok barang', 'apakah barang ini tersedia', 'stok oli, ban, aki',
            'ada aki gs astra', 'stok filter udara', 'ada barang untuk vario',
            'stok kampas kopling', 'cek ketersediaan suku cadang'
        ],
        'daftar_barang': [
            'oli yang tersedia ada apa saja', 'oli apa saja yang ada', 'daftar oli yang tersedia',
            'barang apa yang tersedia', 'jenis sparepart apa saja', 'daftar barang bengkel',
            'produk apa saja ready', 'ada barang apa saat ini', 'apa saja stok yang tersedia',
            'tunjukkan daftar barang', 'daftar suku cadang', 'daftar item bengkel',
            'list barang bengkel', 'barang ready apa saja', 'apa saja item motor',
            'barang senin tersedia', 'daftar jenis oli', 'daftar jenis aki',
            'daftar komponen motor', 'daftar sparepart tersedia', 'daftar produk bengkel'
        ],
        'harga_servis': [
            'ganti oli motor berapa', 'servis motor berapa', 'servis lengkap habis berapa',
            'berapa harga servis', 'biaya service motor', 'berapa ongkos servis',
            'harga ganti aki berapa', 'biaya ganti oli', 'berapa biaya tune up',
            'harga servis motor matic', 'berapa ongkos service', 'harga servis full',
            'berapa harga perbaikan', 'biaya service biasa', 'harga service motor',
            'berapa biaya ganti ban', 'harga servis berkala', 'berapa biaya ganti kampas',
            'biaya servis rem', 'harga servis motor kamu'
        ],
        'info_barang': [
            'informasi oli yamalube matic', 'harga oli ahm mpx 2', 'detail oli enduro matic',
            'info oli terbaik', 'informasi barang', 'info sparepart', 'detail produk motor',
            'apa spesifikasi oli', 'apa kelebihan oli ini', 'info aki gs astra',
            'detail busi iridium', 'info komponen motor', 'detail kampas rem',
            'informasi filter udara', 'info produk bengkel', 'detail produk sparepart',
            'info suku cadang', 'informasi barang motor', 'detail minyak mesin',
            'apa info oli', 'info sparepart motor'
        ],
        'layanan_servis': [
            'motor saya brebet', 'motor brebet saat digas', 'motor brebet di tanjakan',
            'motor tidak hidup', 'motor mati mendadak', 'motor susah distart',
            'motor tersendat', 'motor kurang tenaga', 'motor ngelitik',
            'knalpot motor bunyi', 'rem blong', 'ban bocor', 'motor panas terus',
            'motor hidup mati hidup', 'motor mogok', 'motor tarikan lemah',
            'motor bergetar', 'motor spin gas', 'motor gas tidak stabil',
            'motor susah gas'
        ],
        'rekom_produk': [
            'oli yang cocok untuk beat', 'rekomendasi oli vario', 'oli bagus untuk scoopy',
            'pilih oli untuk nmax', 'pilih oli terbaik untuk honda', 'rekomendasi oli matic',
            'oli untuk motor matik', 'rekomendasi produk motor', 'apa oli terbaik',
            'saran oli untuk vario', 'oli matic apa yang cocok', 'saran produk motor',
            'mana oli yang cocok', 'apa oli untuk beat', 'rekomendasi aki',
            'apa produk terbaik untuk motor', 'saran oli honda', 'rekomendasi sparepart',
            'apa oli ideal untuk nmax', 'saran oli mesin'
        ]
    }
    return templates


def generate_augmentations(df, target_count=240):
    templates = make_templates()
    rows = []
    by_intent = {
        intent: group.iloc[0].to_dict()
        for intent, group in df.groupby('intent')
    }

    for intent, phrases in templates.items():
        base_row = by_intent[intent]
        phrase_pool = expand_phrase_variants(phrases)

        for phrase in phrase_pool:
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
        base_phrases = augmented['pertanyaan'].tolist() or [row['pertanyaan'] for row in rows]

        while len(augmented) + len(extra_rows) < target_count:
            phrase = random.choice(base_phrases)
            candidate = random.choice([
                'tolong ', 'apakah ', 'mohon ', 'saya mau ', 'saya ingin ', 'bagaimana ', ''
            ]) + phrase
            candidate = candidate.strip()
            processed = preprocess_text(candidate)
            if processed and processed not in existing_processed:
                extra_rows.append({
                    'intent': intent,
                    'pertanyaan': candidate,
                    'jawaban': base_row['jawaban'],
                    'action': base_row['action'],
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
        "motor", "bengkel", "servis", "service", "oli", "busi", "aki", "ban",
        "rem", "mesin", "injeksi", "karburator", "sparepart", "stok", "kampas",
        "cvt", "rantai", "lampu", "starter", "brebet", "mogok", "mati", "hidup",
        "panas", "bunyi", "bocor", "gas", "tarikan", "tune", "up", "matic", "beat",
        "vario", "nmax", "scoopy", "pcx", "filter", "udara", "honda", "yamaha",
        "mio", "jadwal", "buka", "jam", "hari", "minggu", "sabtu", "pagi", "siang",
        "sore", "sekarang", "kontak", "admin", "whatsapp", "nomor", "petugas",
        "chat", "produk", "barang", "rekomendasi", "cocok", "bagus", "terbaik",
        "knalpot", "bensin", "tektek", "asap", "putih", "percaya", "dipercaya",
        "murah", "velg", "spion", "cdi", "roller", "switch", "alamat", "rute",
        "maps", "lokasi", "biaya", "ongkos", "tarif", "ngelitik", "goyang",
        "komstir", "stabil", "setang", "stang", "suspensi", "memantul", "keras",
        "drop", "tekor", "selip", "loyo", "gigi", "atas", "tinggi", "rpm", "bawah",
        "langsam", "blong", "piston", "seher", "klep", "noken", "shock", "shockbreaker",
        "karbu", "injektor", "pelek", "radiator", "coolant", "gasket", "paking",
        "kopling", "cakram", "kaliper", "tromol", "spidometer", "speedometer",
        "klakson", "dinamo", "koil", "spul", "kiprok", "ecu", "fuse", "cangklong",
        "accu", "sekring", "bongkar", "pasang", "ganti", "tambah", "kurang", "aus",
        "retak", "patah", "kendor", "kencang", "setel", "stel", "bersihkan",
        "perbaiki", "benerin", "rusak", "ngobos", "ngebul", "kasar", "halus",
        "oleng", "slip", "seret", "macet", "overheat", "tanjakan", "nanjak"
    ]
    text = str(text).lower()
    words = re.findall(r'[a-zA-Z]+', text)
    return any(word in keywords for word in words)


def evaluate_model(vectorizer, model, label_encoder, dataset, test_questions):
    results = []
    for question in test_questions:
        processed = preprocess_text(question)
        x = vectorizer.transform([processed])
        pred = model.predict(x)[0]
        intent = label_encoder.inverse_transform([pred])[0]
        confidence = model.predict_proba(x).max()
        fallback = confidence < 0.10 and intent not in ['sapaan', 'akhir_percakapan', 'bantuan_umum']
        fallback = fallback or (not is_bengkel_domain(question) and intent not in ['sapaan', 'akhir_percakapan', 'bantuan_umum'])
        results.append({
            'question': question,
            'predicted_intent': intent,
            'confidence': float(confidence),
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
    vectorizer, model, label_encoder = train_models(combined)
    print('Retraining complete.')

    test_questions = make_synthetic_questions()
    metrics, results = evaluate_model(vectorizer, model, label_encoder, combined, test_questions)
    print('\n=== Evaluation on 100 synthetic questions ===')
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
