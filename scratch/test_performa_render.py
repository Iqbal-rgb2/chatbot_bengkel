import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from web.app import app

with app.test_client() as client:
    # Simulate login session
    with client.session_transaction() as sess:
        sess['login'] = True
        sess['username'] = 'test_admin'
        
    response = client.get('/performa')
    print(f"Status Code: {response.status_code}")
    html = response.data.decode('utf-8')
    
    # Check for lowest_info contents (since bantuan_umum has lowest F1-score of 64.28%)
    print("Checking if dynamic FAQ title is rendered:")
    if 'Mengapa Topik "Menu Bantuan Chatbot" Kestabilannya Rendah?' in html:
        print("SUCCESS: Dynamic FAQ title rendered correctly!")
    else:
        print("FAIL: Title not found.")
        
    print("\nChecking if dynamic FAQ description is rendered:")
    if 'Topik bantuan umum bersifat sangat luas' in html:
        print("SUCCESS: Dynamic FAQ description rendered correctly!")
    else:
        print("FAIL: Description not found.")
