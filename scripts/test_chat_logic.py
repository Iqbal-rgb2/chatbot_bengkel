import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from web.app import handle_rekomendasi_produk, handle_diagnosa, is_known_diagnosa, handle_list_barang, normalize_user_input

print("=== PENGUJIAN FUNGSI DIAGNOSA ===")
test_diagnose_queries = [
    "motor saya brebet saat digas",
    "motor brebet pas tanjakan",
    "motorku brebet pas nanjak",          # Singkatan 'nanjak' -> 'tanjakan'
    "motorku brebet pas hujan",           # Keluhan umum 'brebet' + modifier dinamis 'hujan'
    "motor saya mogok di jalan",
    "rem depan motor saya blong",
    "knalpot keluar asap putih terus",
    "ada suara bunyi tek-tek di cvt"
]

for query in test_diagnose_queries:
    normalized = normalize_user_input(query)
    is_known = is_known_diagnosa(normalized)
    response = handle_diagnosa(normalized)
    print(f"Query: '{query}' (Normalized: '{normalized}')")
    print(f"  - Terdeteksi keluhan bengkel? {is_known}")
    print(f"  - Respon: {response}\n")

print("=== PENGUJIAN FUNGSI REKOMENDASI PRODUK ===")
test_recom_queries = [
    "rekomendasi oli untuk beat dong",
    "minta rekomendasi oli",
    "rekomendasi sparepart untuk nmax"
]

for query in test_recom_queries:
    normalized = normalize_user_input(query)
    response = handle_rekomendasi_produk(normalized)
    print(f"Query: '{query}' (Normalized: '{normalized}')")
    print(f"  - Respon: {response}\n")

print("=== PENGUJIAN FUNGSI DAFTAR BARANG (handle_list_barang) ===")
test_list_queries = [
    "produk yang ada buat supra apa saja", # Motor saja
    "ada barang apa saja untuk nmax?",    # Motor saja
    "daftar oli yang tersedia apa saja",  # Kategori saja
    "list ban yang cocok buat beat"        # Kategori + Motor
]

for query in test_list_queries:
    normalized = normalize_user_input(query)
    response = handle_list_barang(normalized)
    print(f"Query: '{query}' (Normalized: '{normalized}')")
    print(f"  - Respon: {response}\n")
