# upload_features.py
import requests
from analyze_audio import load_audio, extract_features  # on utilise load_audio pour avoir y et sr
import os

# Chemin absolu ou relatif vers ton fichier
file_path = os.path.expanduser("~/POLYTECH-DISCOver/data/audio/waves.mp3")

# Charger audio
y, sr = load_audio(file_path)

# Extraire les features
features = extract_features(y, sr)

# Préparer payload pour l'API
audio_features = {
    "song_name": "My Song",
    "song_duration_ms": int(features["duration"] * 1000),
    "song_popularity": None,
    "acousticness": features["acousticness"],
    "danceability": features["danceability"],
    "energy": features["energy"],
    "instrumentalness": None,
    "key": None,
    "liveness": None,
    "loudness": None,
    "is_in_data_set": False
}

# Envoi à l'API
response = requests.post(
    "http://localhost:5000/api/v1/songs",
    json=audio_features
)

print(response.json())
