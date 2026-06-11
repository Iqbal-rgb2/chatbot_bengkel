
import requests

BASE = 'http://127.0.0.1:5000'
s = requests.Session()

extra = [
    ('motor nmax saya remnya blong padahal stok kampas ada', 'diagnosa+kompleks'),
    ('saya mau tanya soal transfer bank ke rekening BCA untuk bayar cicilan', 'luar_domain_panjang'),
    ('', 'empty_input'),
    ('abc xyz 123', 'gibberish'),
    ('servis motor matic berapa ongkosnya?', 'harga_servis_matic'),
    ('motor vario saya tarikannya berat', 'diagnosa_tarikan'),
    ('campas rem beat', 'typo_kampas'),
    ('aki lemah', 'diagnosa_aki'),
    ('sedia ban tubeless vario?', 'cek_stok_spesifik'),
    ('mau tanya dong min', 'bantuan_umum'),
]

print('ADDITIONAL EDGE CASES')
print('-'*60)
for question, label in extra:
    r = s.post(BASE + '/chat', json={'message': question})
    d = r.json()
    resp = d.get('response', '')[:100]
    resp_clean = resp.encode('utf-8', errors='replace').decode('utf-8')
    intent = d.get('intent', '')
    conf = d.get('confidence', 0)
    suggestions = d.get('suggestions', [])
    print('[%s]' % label)
    print('  Input    : %r' % question)
    print('  Intent   : %s | Conf: %.3f' % (intent, conf))
    print('  Response : %s...' % resp_clean[:80])
    print('  Saran    : %s' % suggestions)
    print()
