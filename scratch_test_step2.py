import sys
import os
import sqlite3

# Add web directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web'))

from app import normalize_user_input, detect_bad_words, is_bengkel_domain, simpan_log_chat, handle_check_stock

def test_normalization():
    print("--- Test Normalization ---")
    test_cases = {
        "mtr sy brebet": "motor saya brebet",
        "klo bngkl buka jam bwt srvs": "kalau bengkel buka jam buat servis",
        "stk ol motor ready": "stok oli motor ready",
    }
    for inp, expected in test_cases.items():
        res = normalize_user_input(inp)
        print(f"Input: '{inp}' -> Normalized: '{res}'")
        assert expected in res or res in expected, f"Failed normalization! Expected '{expected}' got '{res}'"
    print("Normalization test passed!")

def test_bad_words():
    print("\n--- Test Bad Words ---")
    test_cases = [
        ("woi anjing", True),
        ("tolong bantu saya", False),
        ("dasar brengsek", True),
    ]
    for inp, expected in test_cases:
        res = detect_bad_words(inp)
        print(f"Input: '{inp}' -> Is Bad Word: {res}")
        assert res == expected, f"Failed bad word! Expected {expected} got {res}"
    print("Bad words test passed!")

def test_domain():
    print("\n--- Test Domain ---")
    test_cases = [
        ("piston vario ready?", True),
        ("kiprok beat rusak", True),
        ("apakah besok hujan di surabaya", False),
    ]
    for inp, expected in test_cases:
        res = is_bengkel_domain(inp)
        print(f"Input: '{inp}' -> Is Bengkel Domain: {res}")
        assert res == expected, f"Failed domain check! Expected {expected} got {res}"
    print("Domain test passed!")

def test_product_matching():
    print("\n--- Test Product Matching ---")
    # kiprok is in domain_keywords, but NOT in the DB
    res = handle_check_stock("kiprok varioku rusak, ada ga disini")
    print(f"Result for 'kiprok varioku': '{res}'")
    assert "tidak ditemukan" in res, f"Failed! Expected 'tidak ditemukan' but got: '{res}'"
    print("Product matching false positive test passed!")

def test_auto_classification():
    print("\n--- Test Auto Classification in DB ---")
    # Clean previous test entries if any
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'chatbot.db'))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM log_chat WHERE pertanyaan LIKE 'TEST_AUTO_%'")
    conn.commit()

    # Log 1: fallback_bengkel
    simpan_log_chat("TEST_AUTO_1 piston yamaha", "piston yamaha", "fallback_bengkel", "Pertanyaan Anda masih berkaitan...")
    # Log 2: fallback_luar_bengkel
    simpan_log_chat("TEST_AUTO_2 info cuaca", "info cuaca", "fallback_luar_bengkel", "Pertanyaan Anda di luar lingkup...")
    # Log 3: normal intent
    simpan_log_chat("TEST_AUTO_3 halo", "halo", "sapaan", "Halo! Ada yang bisa dibantu?")

    cursor.execute("SELECT intent, klasifikasi FROM log_chat WHERE pertanyaan LIKE 'TEST_AUTO_%' ORDER BY pertanyaan")
    rows = cursor.fetchall()
    
    print("Fetched classifications:")
    for row in rows:
        print(f"Intent: {row[0]} -> Klasifikasi: {row[1]}")
    
    assert len(rows) == 3
    assert rows[0][1] == 'lingkup_bengkel_belum_ada', f"Log 1 failed: expected 'lingkup_bengkel_belum_ada' got '{rows[0][1]}'"
    assert rows[1][1] == 'melenceng', f"Log 2 failed: expected 'melenceng' got '{rows[1][1]}'"
    assert rows[2][1] == 'ada_di_database', f"Log 3 failed: expected 'ada_di_database' got '{rows[2][1]}'"

    # Clean up test entries
    cursor.execute("DELETE FROM log_chat WHERE pertanyaan LIKE 'TEST_AUTO_%'")
    conn.commit()
    conn.close()
    print("Auto classification DB test passed!")

if __name__ == '__main__':
    test_normalization()
    test_bad_words()
    test_domain()
    test_product_matching()
    test_auto_classification()
    print("\nAll tests completed successfully!")
