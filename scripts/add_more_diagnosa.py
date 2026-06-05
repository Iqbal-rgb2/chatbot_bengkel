import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

new_diagnosa = [
    (
        'mogok starter', 
        'Motor mogok / starter tidak merespon (hanya bunyi cetek-cetek)', 
        'Motor tidak bisa distarter biasanya disebabkan oleh aki lemah, relay starter (bendik) rusak, atau tombol/switch starter kotor.'
    ),
    (
        'mogok kompresi', 
        'Motor mogok dan kick starter terasa sangat enteng (kehilangan kompresi)', 
        'Kondisi loss compression (hilang kompresi) biasanya memerlukan penambahan sedikit oli ke lubang busi untuk merapatkan klep kembali, atau servis besar untuk skir klep.'
    ),
    (
        'rem bunyi', 
        'Rem berdecit atau mengeluarkan suara berisik saat ditekan', 
        'Suara mendecit pada rem disebabkan oleh kampas rem yang kotor terkena debu jalanan atau kampas rem sudah tipis sehingga besi bergesekan dengan piringan cakram.'
    ),
    (
        'rem keras', 
        'Rem terasa keras atau macet saat ditekan', 
        'Rem keras atau macet biasanya disebabkan minyak rem yang kotor/berkurang, piston kaliper macet karena karat, atau terdapat angin palsu di sistem rem.'
    ),
    (
        'bunyi cvt', 
        'Bunyi kasar / berdecit di area CVT matic', 
        'Bunyi kasar di CVT matic umumnya disebabkan oleh roller yang sudah peang/aus, v-belt retak, atau bearing CVT yang mulai oblak.'
    ),
    (
        'bunyi rantai', 
        'Rantai berisik, kendor, atau terasa menyentak', 
        'Rantai berisik biasanya karena kering kurang pelumas, kendor, atau gir roda sudah tajam/aus. Solusinya lakukan pelumasan, penyetelan ulang, atau ganti gir set.'
    ),
    (
        'mesin panas', 
        'Mesin motor cepat panas atau terjadi overheat', 
        'Mesin cepat panas disebabkan oleh air radiator habis (pada motor radiator), kualitas oli menurun karena lama tidak diganti, atau volume oli mesin berkurang drastis.'
    ),
    (
        'asap hitam', 
        'Knalpot motor mengeluarkan asap hitam pekat', 
        'Asap hitam menandakan pembakaran terlalu boros, bisa karena filter udara kotor menyumbat pasokan oksigen, atau setelan karburator/injektor terlalu kaya bensin.'
    )
]

inserted_count = 0
for kata_kunci, gejala, solusi in new_diagnosa:
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO diagnosa_keluhan (kata_kunci, gejala, solusi_analisis) VALUES (?, ?, ?)",
            (kata_kunci, gejala, solusi)
        )
        if cursor.rowcount > 0:
            inserted_count += 1
    except sqlite3.Error as e:
        print(f"Eror saat memasukkan {kata_kunci}: {e}")

conn.commit()
conn.close()

print(f"Berhasil menambahkan {inserted_count} data diagnosa tambahan ke database.")
