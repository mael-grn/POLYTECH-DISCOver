# scripts/test_api.py
import requests

BASE_URL = "http://localhost:5000/api/v1"
HEADERS_JSON = {"Content-Type": "application/json"}

def print_resp(label, resp, expected_status=None):
    status_ok = "✅" if expected_status is None or resp.status_code == expected_status else "❌"
    try:
        data = resp.json()
    except Exception:
        data = resp.text
    print(f"{label}: {status_ok} ({resp.status_code})")
    print(data, end="\n\n")

def main():
    # --- 1) Création utilisateur ---
    user_data = {"name": "TestUser", "email": "test@example.com", "password": "secret123"}
    resp = requests.post(f"{BASE_URL}/users", json=user_data, headers=HEADERS_JSON)
    print_resp("Create user", resp, expected_status=201)
    user_id = resp.json().get("user_id")
    if user_id is None:
        print("Impossible de continuer, user_id manquant !")
        return

    headers_auth = {"X-User-Id": str(user_id), "Content-Type": "application/json"}

    # --- 2) Récupérer son profil ---
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers_auth)
    print_resp("Get me", resp, expected_status=200)

    # --- 3) Création d'une chanson ---
    song_data = {
        "song_name": "Test Song",
        "song_duration_ms": 200000,
        "song_popularity": 50,
        "acousticness": 0.4,
        "danceability": 0.8,
        "energy": 0.7,
    }
    resp = requests.post(f"{BASE_URL}/songs", json=song_data, headers=headers_auth)
    print_resp("Create song", resp, expected_status=201)
    song_id = resp.json().get("song_id")
    if song_id is None:
        print("Impossible de continuer, song_id manquant !")
        return

    # --- 4) Lecture chanson ---
    resp = requests.get(f"{BASE_URL}/songs/{song_id}", headers=headers_auth)
    print_resp("Get song", resp, expected_status=200)

    # --- 5) Upload chanson privée ---
    upload_data = {"song_id": song_id, "private": True}
    resp = requests.post(f"{BASE_URL}/uploads", json=upload_data, headers=headers_auth)
    print_resp("Upload song private", resp, expected_status=201)

    # --- 6) Vérification règles private ---
    resp = requests.get(f"{BASE_URL}/songs/{song_id}")  # sans X-User-Id
    print_resp("Get private song without auth", resp, expected_status=403)

    # --- 7) Mise à jour upload (rendre public) ---
    resp = requests.patch(f"{BASE_URL}/uploads/{song_id}", json={"private": False}, headers=headers_auth)
    print_resp("Patch upload to public", resp, expected_status=200)

    # --- 8) Recherche riche ---
    resp = requests.get(f"{BASE_URL}/songs?q=Test+Song&mode=any", headers=headers_auth)
    print_resp("Search songs", resp, expected_status=200)

    # --- 9) Créer historique ---
    resp = requests.post(f"{BASE_URL}/history", json={"song_id": song_id}, headers=headers_auth)
    print_resp("Create history", resp, expected_status=201)

    # --- 10) Vérifier touch_history ---
    resp = requests.get(f"{BASE_URL}/songs/{song_id}", headers=headers_auth)
    print_resp("Get song to trigger touch_history", resp, expected_status=200)

    resp = requests.get(f"{BASE_URL}/history", headers=headers_auth)
    print_resp("List history", resp, expected_status=200)

    # --- 11) Suppression historique ---
    resp = requests.delete(f"{BASE_URL}/history/{song_id}", headers=headers_auth)
    print_resp("Delete history song", resp, expected_status=200)

    # --- 12) Supprimer chanson et upload ---
    resp = requests.delete(f"{BASE_URL}/songs/{song_id}", headers=headers_auth)
    print_resp("Delete song", resp, expected_status=200)

if __name__ == "__main__":
    main()
