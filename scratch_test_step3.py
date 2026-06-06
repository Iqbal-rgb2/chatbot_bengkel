import sys
import os
import json

# Add web directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web'))

from app import app

def test_chat_response():
    app.config['TESTING'] = True
    client = app.test_client()
    
    # 1. Ambiguous out of domain
    response = client.post('/chat', json=dict(message="apakah hari ini hujan?"))
    data = json.loads(response.data.decode('utf-8'))
    print(f"Query: 'apakah hari ini hujan?' -> Intent: {data['intent']}, Conf: {data['confidence']:.3f}")
    assert data['intent'] == 'fallback_luar_bengkel', f"Expected fallback_luar_bengkel, got {data['intent']}"
    
    # 2. In-domain component not in stock
    response = client.post('/chat', json=dict(message="ada spakbor beat?"))
    data = json.loads(response.data.decode('utf-8'))
    print(f"Query: 'ada spakbor beat?' -> Intent: {data['intent']}, Response: '{data['response'][:60]}...'")
    assert "tidak ditemukan" in data['response'], f"Expected 'tidak ditemukan' in response, got '{data['response']}'"

    # 3. Valid stock check query
    response = client.post('/chat', json=dict(message="stok oli yamalube matic ready?"))
    data = json.loads(response.data.decode('utf-8'))
    print(f"Query: 'stok oli yamalube matic ready?' -> Intent: {data['intent']}, Conf: {data['confidence']:.3f}")
    assert data['intent'] == 'cek_stok', f"Expected cek_stok, got {data['intent']}"
    assert "Stok Oli Yamalube" in data['response'], f"Expected 'Stok Oli Yamalube' in response"

    # 4. Workshop services query
    response = client.post('/chat', json=dict(message="layanan apa saja yang ada di bengkel"))
    data = json.loads(response.data.decode('utf-8'))
    print(f"Query: 'layanan apa saja yang ada di bengkel' -> Intent: {data['intent']}, Response: '{data['response'][:60]}...'")
    assert data['intent'] == 'layanan_servis', f"Expected layanan_servis, got {data['intent']}"
    assert "Servis Motor Matic" in data['response'], f"Expected service list in response, got '{data['response']}'"

    print("\n[SUCCESS] All Step 3 checks passed successfully!")

if __name__ == '__main__':
    test_chat_response()
