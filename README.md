# 🏍️ Chatbot Layanan Informasi Bengkel Motor Kurnia

> **Proyek Tugas Akhir / Skripsi**  
> **Judul:** Pengembangan Chatbot Bengkel Motor Kurnia Berbasis NLP Menggunakan Metode TF-IDF dan Naive Bayes  
> **Oleh:** Muhammad Iqbal (NIM: 222140029)  
> **Program Studi:** Informatika, Fakultas Teknik dan Informatika, Institut Teknologi dan Bisnis Widya Gama Lumajang  

---

## 📌 Deskripsi Proyek
Proyek ini merupakan sistem layanan informasi otomatis (*chatbot*) berbasis web yang dirancang khusus untuk membantu pelanggan **Bengkel Motor Kurnia Senduro** dalam memperoleh informasi secara cepat, akurat, dan responsif selama 24 jam. 

Sistem ini mengimplementasikan pendekatan **Natural Language Processing (NLP)** dengan metode representasi teks **TF-IDF** (*Term Frequency-Inverse Document Frequency*) dan algoritma klasifikasi **Multinomial Naive Bayes (MultinomialNB)** untuk mengenali maksud (*intent*) dari pertanyaan bahasa alami pelanggan.

---

## 🚀 Fitur Utama
1. **Klasifikasi 12 Kelas Intent:** Chatbot dapat mendeteksi secara otomatis 12 kategori topik pertanyaan pelanggan:
   * `sapaan`, `bantuan_umum`, `jadwal_bengkel`, `lokasi_bengkel`, `kontak_admin`, `harga_servis`, `layanan_servis` (diagnosa keluhan), `daftar_barang`, `cek_stok`, `info_barang`, `rekom_produk`, dan `akhir_percakapan`.
2. **Gerbang Keamanan Hibrida (Hybrid Security Gate):**
   * Menggabungkan probabilitas Naive Bayes dengan perhitungan kemiripan vektor **Cosine Similarity** terhadap kalimat latih di database.
   * Mampu menolak pertanyaan di luar domain (*out-of-domain*) dan mengarahkan keluhan tak terdaftar ke tombol pintasan WhatsApp Admin secara otomatis (*in-domain fallback*).
3. **Koneksi Database SQLite Real-Time (Dynamic Action):**
   * **Cek Stok Otomatis:** Menarik jumlah sisa suku cadang real-time dari database.
   * **Info Detail Produk:** Menyajikan info spesifikasi produk dan harganya.
   * **Rekomendasi Produk:** Memberikan saran tipe oli atau ban yang cocok untuk jenis motor tertentu.
4. **Dasbor Administrasi Petugas (Admin Dashboard):**
   * Panel kelola stok barang langsung maupun berbasis rumpun mesin motor (Matic, Bebek, Sport).
   * Perekaman log riwayat perubahan stok suku cadang secara otomatis oleh admin.
   * Perekaman dan pemantauan log chat riwayat percakapan pengguna.
   * **Visualisasi Metrik Performa:** Menampilkan grafik akurasi sistem (**93.46%**), Confusion Matrix, dan FAQ panduan evaluasi performa model di halaman dashboard.

---

## 🛠️ Spesifikasi Teknologi (Tech Stack)
* **Backend Framework:** Python 3.12, Flask
* **Machine Learning / NLP:** Scikit-learn (`TfidfVectorizer`, `MultinomialNB`), NLTK/difflib (`get_close_matches`), Pustaka Stemmer Sastrawi
* **Database Engine:** SQLite3 (Local file-based database)
* **Frontend:** HTML5, CSS3 (Vanilla CSS), JavaScript (AJAX fetch API untuk obrolan dinamis tanpa reload halaman)

---

## 📂 Struktur Direktori Proyek
```text
chatbot_bengkel/
├── data/                    # Dataset pelatihan (dataset_clean.csv, dataset_augmented.csv)
├── database/                # Database SQLite3 (chatbot.db) & skrip SQL seed
├── models/                  # File serialisasi model machine learning (.joblib) & Confusion Matrix
├── scripts/                 # CLI Python scripts (db_manager.py, augment_and_retrain.py)
├── web/                     # Modul aplikasi Flask (app.py, routes, nlp, templates, static)
├── DEVELOPMENT.md           # Dokumen panduan detail teknis pengembang (development guide)
├── requirements.txt         # File dependensi/pustaka Python yang diperlukan
└── README.md                # Dokumentasi beranda utama proyek ini
```

---

## ⚡ Panduan Instalasi & Menjalankan Chatbot

Ikuti langkah-langkah di bawah ini untuk menjalankan chatbot secara lokal pada komputer Anda:

### 1. Kloning Repositori
```bash
git clone https://github.com/Iqbal-rgb2/chatbot_bengkel.git
cd chatbot_bengkel
```

### 2. Buat dan Aktifkan Virtual Environment (venv)
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

### 3. Install Dependensi Pustaka
```bash
pip install -r requirements.txt
```

### 4. Inisialisasi Database & Seeder
Buat berkas database lokal SQLite beserta seluruh data seed awal:
```bash
python scripts/db_manager.py --init
```

### 5. Jalankan Server Flask
```bash
python web/app.py
```
Buka peramban (browser) Anda dan akses alamat:  
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 📖 Panduan Lanjutan
Untuk panduan detail alur kerja pengembang seperti **menambah dataset**, **melatih ulang model NLP**, atau **mencadangkan perubahan database ke berkas SQL**, silakan baca dokumen panduan lengkap di:  
📄 **[DEVELOPMENT.md](DEVELOPMENT.md)**
