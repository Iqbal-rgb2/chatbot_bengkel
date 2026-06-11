import sys
import os

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console with emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add web directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web'))

from app import app, check_conversational_context, handle_diagnosa, handle_list_barang, handle_rekomendasi_produk

def run_tests():
    print("=== STARTING KEYWORD MATCHING BUG FIX TESTS ===")
    
    # 1. Test conversational context checker false positive fixes
    with app.test_request_context():
        session = {} # stub or use Flask session
        from flask import session
        session['last_suggestions'] = ["Alamat & Rute Maps", "Hubungi WhatsApp"]
        
        # "ada ban gak" contains "gak", but it's not a rejection. Should NOT intercept.
        query_cf, direct_cf = check_conversational_context("ada ban gak")
        print(f"Query: 'ada ban gak' -> Target: {query_cf}, Direct: {direct_cf}")
        assert direct_cf is None, "Failed! 'ada ban gak' was incorrectly intercepted as a rejection."
        
        # "ganti ban" contains "ga" (substring of ganti), but is not a rejection. Should NOT intercept.
        query_cf2, direct_cf2 = check_conversational_context("ganti ban")
        print(f"Query: 'ganti ban' -> Target: {query_cf2}, Direct: {direct_cf2}")
        assert direct_cf2 is None, "Failed! 'ganti ban' was incorrectly intercepted as a rejection."
        
        # "tidak" is a direct rejection. Should intercept.
        query_cf3, direct_cf3 = check_conversational_context("tidak")
        print(f"Query: 'tidak' -> Target: {query_cf3}, Direct: '{direct_cf3[0] if direct_cf3 else None}'")
        assert direct_cf3 is not None, "Failed! 'tidak' was not intercepted as a rejection."
        
    print("Conversational Context Checker tests passed!")
    
    # 2. Test handle_diagnosa false positive fixes
    # "oli rembes" contains "rem" as a substring. Should NOT trigger rem diagnosa.
    res_diag = handle_diagnosa("oli rembes")
    print(f"Query: 'oli rembes' -> Diagnosa: '{res_diag}'")
    assert "rem" not in res_diag and "detail" in res_diag.lower(), "Failed! 'oli rembes' was incorrectly diagnosed as a brake (rem) issue."
    
    # "rem blong" contains exact word "rem". Should trigger rem diagnosa.
    res_diag2 = handle_diagnosa("rem blong")
    print(f"Query: 'rem blong' -> Diagnosa: '{res_diag2[:60]}...'")
    assert "rem" in res_diag2.lower() and "detail" not in res_diag2.lower(), "Failed! 'rem blong' did not trigger a brake (rem) diagnosa."
    
    # 3. Test handle_list_barang false positive fixes
    # "bengkel di bandung" contains "ban" as a substring. Should NOT match category "ban".
    res_list = handle_list_barang("bengkel di bandung")
    print(f"Query: 'bengkel di bandung' -> List: '{res_list}'")
    assert "Kategori" in res_list or "Barang yang" in res_list, "Failed! 'bengkel di bandung' was incorrectly matched to category 'ban'."
    
    # "stok ban beat" contains exact word "ban". Should match category "ban".
    res_list2 = handle_list_barang("stok ban beat")
    print(f"Query: 'stok ban beat' -> List: '{res_list2[:60]}...'")
    assert "Kategori" not in res_list2 and "ban" in res_list2.lower(), "Failed! 'stok ban beat' did not match category 'ban'."

    print("Keyword and category/motor matching tests passed!")
    print("\n[ALL FIXES SUCCESSFULLY VERIFIED]")

if __name__ == '__main__':
    run_tests()
