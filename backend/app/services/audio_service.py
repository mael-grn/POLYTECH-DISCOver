# backend/app/services/audio_service.py
import os
import numpy as np
import librosa
from pathlib import Path
from app.models.song import Song

# Génération de caractéristiques audio à partir de fichiers audio



class AudioAnalysisService:
    def __init__(self):
        pass

    @staticmethod
    def _estimate_mode_major_minor(chroma_mean: np.ndarray) -> int | None: #determine la tonalité de la musique
        major = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


        c = chroma_mean / (np.linalg.norm(chroma_mean) + 1e-9) 
        maj = major / np.linalg.norm(major) 
        minr = minor / np.linalg.norm(minor)


        best_maj = -1e9
        best_min = -1e9
        for shift in range(12): #on teste les 12 tonalités possibles
            maj_s = np.roll(maj, shift)
            min_s = np.roll(minr, shift)
            best_maj = max(best_maj, float(np.dot(c, maj_s)))
            best_min = max(best_min, float(np.dot(c, min_s)))

        return 1 if best_maj >= best_min else 0 #1 pour majeur, 0 pour mineur

    def analyze_file(self, file_path: str, song_title: str = None) -> Song | None: #permet d'analyser et extraire les caractéristiques d'un morceau
        if not os.path.exists(file_path):
            print(f"Fichier introuvable : {file_path}")
            return None

        try:

            y, sr = librosa.load(file_path, mono=True) 

            if y is None or len(y) < sr * 1:
                print("Audio trop court ou vide.")
                return None


            duration_sec = librosa.get_duration(y=y, sr=sr) #récupération de la durée en secondes
            duration_ms = int(duration_sec * 1000)


            tempo, _ = librosa.beat.beat_track(y=y, sr=sr) #récupération du tempo en BPM
            bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])


            chroma = librosa.feature.chroma_stft(y=y, sr=sr) #récupération de la tonalité
            chroma_mean = np.mean(chroma, axis=1)
            key = int(np.argmax(chroma_mean))                #note fondamentale (0=C, 1=C#, ..., 11=B)
            audio_mode = self._estimate_mode_major_minor(chroma_mean)


            rms = librosa.feature.rms(y=y)[0]                 #récupération de la puissance sonore
            rms_mean = float(np.mean(rms))
            loudness_db = float(20.0 * np.log10(max(rms_mean, 1e-9)))


            time_signature = 4


            acousticness = None   #caractéristiques non calculées avec librosa
            danceability = None
            energy = None
            instrumentalness = None
            liveness = None
            speechiness = None
            audio_valence = None

            final_title = song_title if song_title else Path(file_path).stem

            return Song(  #création de l'objet Song avec les caractéristiques extraites
                song_name=final_title,
                song_popularity=None,
                song_duration_ms=duration_ms,

                acousticness=acousticness,
                danceability=danceability,
                energy=energy,
                instrumentalness=instrumentalness,
                key=key,
                liveness=liveness,
                loudness=round(loudness_db, 3),

                audio_mode=audio_mode,
                speechiness=speechiness,
                tempo=round(bpm, 3),
                time_signature=time_signature,
                audio_valence=audio_valence,

                is_in_data_set=False
            )

        except Exception as e:
            print(f"Erreur lors de l'analyse audio : {e}")
            return None
