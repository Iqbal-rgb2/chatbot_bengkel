import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

even_more_diagnosa = [
    (
        'brebet panas',
        'Motor brebet saat mesin panas',
        'Motor brebet saat kondisi mesin panas biasanya karena koil pengapian mulai lemah/terlalu panas, atau setelan klep terlalu rapat sehingga tidak ada celah saat memuai.'
    ),
    (
        'brebet hujan',
        'Motor brebet setelah kehujanan atau terkena air',
        'Motor brebet setelah kehujanan atau terkena air biasanya disebabkan cop busi (cangklong busi) bocor sehingga air masuk, atau kabel pengapian terkelupas.'
    ),
    (
        'brebet atas',
        'Motor brebet di putaran atas / RPM tinggi',
        'Motor brebet pada putaran atas / RPM tinggi umumnya disebabkan main jet karburator tersumbat, filter udara sangat kotor, atau pasokan bahan bakar dari pompa bensin (fuel pump) melemah.'
    ),
    (
        'brebet bawah',
        'Motor brebet di putaran bawah / langsam tidak stabil',
        'Motor brebet pada putaran bawah / langsam tidak stabil biasanya karena pilot jet karburator tersumbat, setelan sekrup udara kurang pas, atau terjadi kebocoran udara di manifol karburator.'
    ),
    (
        'rem blong',
        'Rem blong atau tidak pakem sama sekali',
        'Rem blong atau tidak pakem disebabkan kampas rem habis total, minyak rem habis/bocor, piston kaliper macet karena karat, atau terjadi vapor lock (minyak rem mendidih).'
    ),
    (
        'stang goyang',
        'Stang motor terasa goyang, tidak stabil, atau membuang ke samping',
        'Stang terasa goyang atau tidak stabil biasanya karena komstir (steering head) yang aus/kendor, velg baling, ban benjol/kurang angin, atau bearing (laker) tromol roda oblak.'
    ),
    (
        'shock bocor',
        'Shockbreaker keras, memantul berlebihan, atau bocor oli',
        'Shockbreaker terasa keras atau memantul berlebihan disebabkan oleh oli shock bocor/habis, seal shock rusak, atau per suspensi sudah lemah sehingga suspensi mentok (bottoming).'
    ),
    (
        'aki tekor',
        'Aki sering drop, tekor, atau tidak bisa menyimpan daya',
        'Aki sering tekor umumnya disebabkan oleh sistem pengisian (kiprok/spool) yang bermasalah, adanya korsleting kabel (kebocoran arus), atau umur sel aki yang memang sudah habis.'
    ),
    (
        'kopling selip',
        'Kopling terasa selip, tarikan mesin loyo, atau gigi susah masuk',
        'Kopling selip atau tarikan mesin loyo disebabkan oleh kampas kopling yang aus/gosong, plat kopling melengkung, atau per kopling yang mulai melemah.'
    ),
    (
        'mesin ngelitik',
        'Mesin berbunyi ngelitik (knocking) saat akselerasi atau digas',
        'Mesin berbunyi ngelitik (knocking) umumnya disebabkan penggunaan bahan bakar dengan oktan terlalu rendah, penumpukan kerak karbon di ruang bakar, atau setelan celah klep yang terlalu renggang.'
    )
]

inserted_count = 0
for kata_kunci, gejala, solusi in even_more_diagnosa:
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO diagnosa_keluhan (kata_kunci, gejala, solusi_analisis) VALUES (?, ?, ?)",
            (kata_kunci, gejala, solusi)
        )
        if cursor.rowcount > 0:
            inserted_count += 1
        else:
            # Jika sudah ada kata_kunci tersebut, lakukan update untuk memastikan solusinya paling lengkap
            cursor.execute(
                "UPDATE diagnosa_keluhan SET gejala = ?, solusi_analisis = ? WHERE kata_kunci = ?",
                (gejala, solusi, kata_kunci)
            )
            if cursor.rowcount > 0:
                inserted_count += 1
    except sqlite3.Error as e:
        print(f"Eror saat memasukkan/mengupdate {kata_kunci}: {e}")

conn.commit()
conn.close()

print(f"Berhasil mengupdate database! {inserted_count} data diagnosa spesifik telah diperbarui/ditambahkan.")
