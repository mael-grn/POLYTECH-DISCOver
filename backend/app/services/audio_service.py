# backend/app/services/audio_service.py
import librosa
import numpy as np
import os
from app.models.song import Song


class AudioAnalysisService:
    def __init__(self):
        pass

    def analyze_file(self, file_path: str, song_title: str = None) -> Song | None:
        """
        Analyse un fichier audio local (.mp3, .wav) et retourne un objet Song.
        """
        if not os.path.exists(file_path):
            print(f"Fichier introuvable : {file_path}")
            return None

        try:
            # 1. Chargement du fichier audio
            y, sr = librosa.load(file_path)

            # ---Récupération des données---

            # Durée en ms
            duration_sec = librosa.get_duration(y=y, sr=sr)
            duration_ms = int(duration_sec * 1000)

            # Loudness (dB)
            # On calcule l'énergie moyenne (RMS) et on convertit en dB
            rms = librosa.feature.rms(y=y)
            loudness = float(librosa.amplitude_to_db(rms).mean())

            # Tempo (BPM)
            tempo_array, _ = librosa.beat.beat_track(y=y, sr=sr)
            # beat_track peut retourner un float ou un array, on sécurise
            bpm = float(tempo_array) if np.isscalar(tempo_array) else float(tempo_array[0])

            # Key (Tonalité)
            # Chromagramme pour détecter la note dominante
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            # On fait la moyenne pour trouver la classe de note dominante (0=Do, 1=Do#, etc.)
            key = int(np.argmax(np.mean(chroma, axis=1)))

            # ---Estimation des features (Heuristiques)---

            # Energy (0.0 à 1.0)
            # On normalise le RMS. Supposons qu'un RMS de 0.2 est une énergie max "standard"
            raw_energy = float(np.mean(rms))
            energy = min(raw_energy * 5, 1.0)  # Facteur *5 arbitraire pour échelonner

            # Danceability (0.0 à 1.0)
            # Basé sur la stabilité du rythme. Plus le rythme est clair, plus c'est dansant.
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
            # Si le tempo est entre 90 et 130 BPM (pop/dance), on booste le score
            dance_score = pulse.mean()
            if 90 < bpm < 140:
                dance_score *= 1.2
            danceability = min(dance_score, 1.0)

            # Acousticness / Instrumentalness / Liveness
            # Difficile à calculer
            # On met des valeurs par défaut ou des calculs très simples (Spectral Rolloff)
            # Le spectral rolloff est bas pour les sons acoustiques/sombres
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
            # Normalisation très brute : plus le son est "brillant" (hautes fréquences), moins il est acoustique
            acousticness = max(0.0, 1.0 - (rolloff / 3000))
            audio_mode = None
            speechiness = None
            time_signature = 4
            audio_valence = None
            # --- Création de l'objet Song ---

            # Si aucun titre n'est fourni, on prend le nom du fichier
            final_title = song_title if song_title else os.path.basename(file_path)

            new_song = Song(
                song_name=final_title,
                song_popularity=None,  # Inconnu car pas encore sorti
                song_duration_ms=duration_ms,

                acousticness=round(acousticness, 3),
                danceability=round(danceability, 3),
                energy=round(energy, 3),
                instrumentalness=0.0,  # Trop dur à deviner avec librosa
                key=key,
                liveness=0.0,  # Trop dur à deviner avec librosa
                loudness=round(loudness, 3),
                audio_mode=audio_mode,
                tempo=round(bpm, 3),
                speechiness=speechiness,
                time_signature=time_signature,
                audio_valence=audio_valence,
                is_in_data_set=False
            )

            return new_song

        except Exception as e:
            print(f"Erreur lors de l'analyse audio : {e}")
            return None