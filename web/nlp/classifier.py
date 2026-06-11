import re
import pandas as pd
import joblib
from web.config import (
    DATA_PATH, VECTORIZER_PATH, MODEL_PATH, LABEL_PATH,
    THRESHOLD_NAIVE_BAYES, THRESHOLD_COSINE_SIMILARITY
)
from web.nlp.preprocessor import bad_words

# =====================================
# LOAD DATASET & MODELS
# =====================================
df = pd.read_csv(DATA_PATH)
df = df.fillna('')

vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_PATH)

# =====================================
# KEYWORD DOMAIN BENGKEL
# =====================================
domain_keywords = [
    "motor", "bengkel", "servis", "service", "layanan", "oli", "busi", "aki", "ban", "rem",
    "mesin", "injeksi", "karburator", "sparepart", "stok", "kampas", "cvt", "rantai", "lampu",
    "starter", "brebet", "mogok", "mati", "hidup", "panas", "bunyi", "bocor", "gas", "tarikan",
    "tune", "up", "matic", "beat", "vario", "nmax", "scoopy", "pcx", "filter", "udara", "honda",
    "yamaha", "mio", "jadwal", "buka", "jam", "minggu", "sabtu", "kontak", "admin", "whatsapp",
    "nomor", "petugas", "chat", "produk", "barang", "rekomendasi", "cocok", "bagus", "terbaik",
    "knalpot", "bensin", "tektek", "asap", "putih", "percaya", "dipercaya", "murah", "velg",
    "spion", "cdi", "roller", "switch", "alamat", "rute", "maps", "lokasi", "biaya", "ongkos",
    "tarif", "ngelitik", "goyang", "komstir", "stabil", "setang", "stang", "suspensi", "memantul",
    "keras", "drop", "tekor", "selip", "loyo", "gigi", "atas", "tinggi", "rpm", "bawah", "langsam",
    "blong", "piston", "seher", "klep", "noken", "shock", "shockbreaker", "karbu", "injektor",
    "pelek", "radiator", "coolant", "gasket", "paking", "kopling", "cakram", "kaliper", "tromol",
    "spidometer", "speedometer", "klakson", "dinamo", "koil", "spul", "kiprok", "ecu", "fuse",
    "cangklong", "accu", "sekring", "bongkar", "pasang", "ganti", "tambah", "kurang", "aus",
    "retak", "patah", "kendor", "kencang", "setel", "stel", "bersihkan", "perbaiki", "benerin",
    "rusak", "ngobos", "ngebul", "kasar", "halus", "oleng", "slip", "seret", "macet", "overheat",
    "tanjakan", "nanjak"
]

# =====================================
# DETEKSI KATA KASAR
# =====================================
def detect_bad_words(text):
    text = text.lower()
    for word in bad_words:
        if word in text:
            return True
    return False

# =====================================
# DETEKSI DOMAIN BENGKEL
# =====================================
def is_bengkel_domain(text):
    text = str(text).lower()
    words = re.findall(
        r'[a-zA-Z]+',
        text
    )

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

    for word in words:
        if word in domain_keywords:
            return True

    return False

# =====================================
# RESPONSE FALLBACK
# =====================================
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

# =====================================
# PRIORITAS INTENT BERDASARKAN KEYWORD
# =====================================
def contains_any(text, keywords):
    text_lower = str(text).lower()
    words = set(re.findall(r'[a-zA-Z]+', text_lower))
    for keyword in keywords:
        kw_lower = keyword.lower()
        if ' ' in kw_lower:
            if kw_lower in text_lower:
                return True
        else:
            if kw_lower in words:
                return True
    return False

def prioritize_intent(text, predicted_intent):
    text_lower = str(text).lower()

    # 1. AKHIR PERCAKAPAN
    if contains_any(text_lower, ["terima kasih", "makasih", "matur nuwun", "thanks", "thank you", "bye", "cukup"]) or "cukup ya" in text_lower or "udah cukup" in text_lower or "sudah cukup" in text_lower:
        return "akhir_percakapan"

    # 2. BANTUAN UMUM
    if contains_any(text_lower, ["bantu", "bantuan", "nanya", "tanya"]) and contains_any(text_lower, ["saya", "admin", "min", "dong", "tolong"]):
        return "bantuan_umum"

    # 3. SAPAAN - only override if it doesn't contain other strong intent keywords
    sapaan_keywords = ["halo", "hai", "hallo", "selamat", "salam", "assalamualaikum", "permisi", "punten", "pagi", "siang", "sore", "malam"]
    exclude_sapaan = [
        "admin", "servis", "service", "stok", "harga", "biaya", "alamat", "lokasi", 
        "tutup", "buka", "jam", "wa", "whatsapp", "nomor", "no", "rekomendasi", 
        "oli", "ban", "aki", "busi", "rem", "jasa", "ongkos", "tarif", "berapa", "bayar"
    ]
    if contains_any(text_lower, sapaan_keywords) and not contains_any(text_lower, exclude_sapaan):
        return "sapaan"

    # Product keywords
    product_keywords = [
        "barang", "produk", "sparepart", "oli", "busi", "aki", "ban", "kampas",
        "rem", "cakram", "kaliper", "tromol", "lampu", "velg", "knalpot", "filter",
        "udara", "karburator", "cdi", "spion", "roller", "switch", "starter",
        "honda", "yamaha", "mio", "beat", "vario", "nmax", "pcx", "scoopy"
    ]

    # 4. BANTUAN UMUM (bengkel-specific general help)
    if contains_any(text_lower, ["percaya", "dipercaya", "terpercaya", "murah"]) and contains_any(text_lower, ["bengkel"]):
        return "bantuan_umum"

    # 5. LAYANAN SERVIS (keluhan)
    if contains_any(text_lower, ["mogok", "brebet", "rem", "mesin", "bensin", "asap", "bunyi", "tektek"]) and not contains_any(text_lower, ["harga", "biaya", "kampas"]):
        return "layanan_servis"

    # 6. HARGA SERVIS
    harga_servis_keywords = ["harga", "biaya", "ongkos", "tarif", "berapa", "bayar", "tarifnya"]
    service_action_keywords = ["servis", "service", "tune", "up", "ganti", "perbaikan", "benerin", "perbaiki"]
    if contains_any(text_lower, harga_servis_keywords) and contains_any(text_lower, service_action_keywords):
        return "harga_servis"

    # 7. LAYANAN SERVIS (jasa servis umum)
    if contains_any(text_lower, ["layanan", "jasa", "servis", "service"]) and not contains_any(text_lower, product_keywords + ["harga", "biaya", "bantu", "terima kasih"]):
        return "layanan_servis"

    # 8. DAFTAR BARANG
    if (
        contains_any(text_lower, ["daftar", "list", "jenis", "pilihan"])
        or "ada apa saja" in text_lower
        or "apa saja" in text_lower
    ) and contains_any(text_lower, product_keywords):
        return "daftar_barang"

    # 9. KONTAK ADMIN
    if contains_any(text_lower, ["whatsapp", "wa", "telepon", "telp", "phone", "kontak", "hubungi", "petugas"]) or (
        "nomor" in text_lower and contains_any(text_lower, ["admin", "wa", "whatsapp", "bengkel", "petugas", "hp", "telp"])
    ) or (
        "chat" in text_lower and contains_any(text_lower, ["admin", "petugas", "bengkel"])
    ):
        return "kontak_admin"

    # 10. JADWAL BENGKEL
    if contains_any(text_lower, ["jadwal", "jam operasional", "operasional", "buka jam", "tutup jam", "jam kerja", "hari kerja"]) or (
        contains_any(text_lower, ["buka", "tutup", "buka tidak", "buka gak"])
        and contains_any(text_lower, ["hari", "minggu", "sabtu", "senin", "selasa", "rabu", "kamis", "jumat", "sekarang", "besok", "sore", "pagi"])
    ):
        return "jadwal_bengkel"

    # 11. REKOMENDASI PRODUK
    if (
        contains_any(text_lower, ["rekomendasi", "cocok", "bagus", "terbaik"])
        or ("oli untuk" in text_lower and contains_any(text_lower, product_keywords))
    ) and not contains_any(text_lower, ["harga", "biaya", "berapa"]):
        return "rekom_produk"

    # 12. CEK STOK
    if contains_any(text_lower, ["stok", "tersedia", "ada", "sedia", "cek", "ready"]) and contains_any(text_lower, product_keywords) and not contains_any(text_lower, ["harga", "biaya", "berapa"]):
        return "cek_stok"

    # 13. INFO BARANG
    if contains_any(text_lower, ["informasi", "info", "detail", "spesifikasi", "harga", "berapa"]) and contains_any(text_lower, product_keywords):
        return "info_barang"

    return predicted_intent

