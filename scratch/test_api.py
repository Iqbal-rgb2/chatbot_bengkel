import requests, json, sys

def print_section(title, content):
    print(f"=== {title} ===")
    print(content)
    print()

base_url = 'http://127.0.0.1:5000'

# Home page
resp = requests.get(base_url + '/')
print_section('HOME STATUS', resp.status_code)
print_section('HOME CONTENT', resp.text[:500])

# Chat endpoint with sample messages
def chat(message):
    r = requests.post(base_url + '/chat', json={'message': message})
    return r.json()

samples = [
    "Halo",
    "Ada oli?",
    "Berapa harga ban?",
    "Saya ingin diagnosis motor",
    "Terima kasih",
]
for msg in samples:
    result = chat(msg)
    print_section(f'CHAT RESPONSE for "{msg}"', json.dumps(result, ensure_ascii=False, indent=2))

# Admin login (GET login page)
resp_login = requests.get(base_url + '/login')
print_section('ADMIN LOGIN PAGE STATUS', resp_login.status_code)

# Dashboard (requires session, cannot login without credentials; skip)
