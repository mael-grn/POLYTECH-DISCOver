import librosa
import numpy as np
from pydub import AudioSegment

def load_audio(file_path: str, target_sr=22050):
    """
    Charge le fichier audio et retourne le signal + sample rate.
    """
    # Conversion MP4 -> WAV si besoin
    if file_path.lower().endswith((".mp4", ".m4a")):
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")
        file_path = wav_path

    # Charger l'audio avec librosa
    y, sr = librosa.load(file_path, sr=target_sr, mono=True)
    return y, sr

def extract_features(y, sr):
    """
    Extrait les features audio principales.
    """
    features = {}

    # Durée
    features["duration"] = float(librosa.get_duration(y=y, sr=sr))

    # Tempo (bpm)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    features["tempo"] = float(tempo[0])

    # Energie (root-mean-square)
    rmse = librosa.feature.rms(y=y)
    features["energy"] = float(np.mean(rmse))

    # Danceability approximée par régularité du tempo et énergie
    features["danceability"] = float(np.clip(features["energy"] * (tempo[0] / 200), 0, 1))

    # Valence approximée par tonalité majeure vs mineure
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features["valence"] = float(np.mean(chroma))  # approximation

    # Acousticness approximée par spectre hautes fréquences
    S = np.abs(librosa.stft(y))
    high_freq_ratio = np.mean(S[1000:, :] / (np.mean(S, axis=0) + 1e-6))
    features["acousticness"] = float(np.clip(1 - high_freq_ratio, 0, 1))

    return features

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python analyze_audio.py <file.mp3/mp4>")
        sys.exit(1)

    file_path = sys.argv[1]
    y, sr = load_audio(file_path)
    features = extract_features(y, sr)

    # Affichage JSON sûr
    print(json.dumps(features, indent=2))
