# backend/app/services/audio_service.py
import os
import numpy as np
import librosa
from pathlib import Path
from app.models.song import Song

# Service d'analyse d'audio
class AudioAnalysisService:
    # Initialisation
    def __init__(self):
        pass

    @staticmethod
    def _estimate_mode_major_minor(chroma_mean: np.ndarray) -> int | None:
        """
        Estimation de la tonalité majeure ou mineure d'une chanson à partir de son chroma moyen.

        - chroma_mean : Vecteur représentant l'intensité moyenne.
        - retourne :
            - 1 si la chanson est estimée en tonalité majeure,
            - 0 si la chanson est estimée en tonalité mineure.
        """
        # Tonalité majeure
        major = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        # Tonalité mineure
        minor = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        # Normalisation des tonalités de la chanson
        c = chroma_mean / (np.linalg.norm(chroma_mean) + 1e-9)
        # Normalisation des tonalités majeures
        maj = major / np.linalg.norm(major)
        # Normalisation des tonalités mineures
        minr = minor / np.linalg.norm(minor)

        # Initialisation du meilleur score majeur
        best_maj = -1e9
        # Initialisation du meilleur score mineur
        best_min = -1e9
        # Boucle sur les transpositions
        for shift in range(12):
            # Décalage circulaire du profil majeur
            maj_s = np.roll(maj, shift)
            # Décalage circulaire du profil mineur
            min_s = np.roll(minr, shift)
            # Actualisation du meilleur score majeur en fonction de chaque transposition
            best_maj = max(best_maj, float(np.dot(c, maj_s)))
            # Actualisation du meilleur score mineur en fonction de chaque transposition
            best_min = max(best_min, float(np.dot(c, min_s)))

        # Retourne 1 si la chanson est plus de tonalité majeure, et 0 sinon
        return 1 if best_maj >= best_min else 0

    def analyze_file(self, file_path: str, song_title: str = None) -> Song | None:
        """
        Analyse d'un fichier audio et extraction de ses caractéristiques musicales.

        - file_path : chemin vers le fichier audio à analyser
        - song_title : nom de la chanson à utiliser
        - retourne :
            - Un objet Song contenant les caractéristiques extraites si l'analyse réussit
            - None si le fichier est invalide, trop court, ou si une erreur se produit.
        """
        # Si le fichier n'existe pas dans l'OS, arrêter la fonction
        if not os.path.exists(file_path):
            print(f"Fichier introuvable : {file_path}")
            return None

        try:
            # Chargement du fichier audio
            y, sr = librosa.load(file_path, mono=True)

            # Si le fichier est vide ou qu'il dure moins d'une seconde, arrêter la fonction
            if y is None or len(y) < sr * 1:
                print("Audio trop court ou vide.")
                return None

            # Récupérer la durée de l'audio en secondes
            duration_sec = librosa.get_duration(y=y, sr=sr)
            # Récupérer la durée de l'audio en millisecondes
            duration_ms = int(duration_sec * 1000)

            # Récupération du tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            # Actualisation du tempo en battements par minutes
            bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])

            # Récupération de la tonalité
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            # Moyenne de tonalité
            chroma_mean = np.mean(chroma, axis=1)
            # Index de la note la plus forte
            key = int(np.argmax(chroma_mean))
            # Estimation de la tonalité de la chanson
            audio_mode = self._estimate_mode_major_minor(chroma_mean)

            # Récupération de l'amplitude
            rms = librosa.feature.rms(y=y)[0]
            # Moyenne de l'amplitude
            rms_mean = float(np.mean(rms))
            # Conversion de l'amplitude en décibels
            loudness_db = float(20.0 * np.log10(max(rms_mean, 1e-9)))

            # Initialisation de la signature rythmique à 4
            time_signature = 4

            # Initialisation de l'acoustiquité, la dançabilité, l'énergie, l'instrumentalité, la vie, la verbalité, et la valence de l'audio à None
            acousticness = None
            danceability = None
            energy = None
            instrumentalness = None
            liveness = None
            speechiness = None
            audio_valence = None

            # Récupération du nom de la chanson
            final_title = song_title if song_title else Path(file_path).stem

            # Retour de la chanson avec les caractéristiques précédentes
            return Song(
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
        # Si une erreur se produit, arrêter la fonction
        except Exception as e:
            print(f"Erreur lors de l'analyse audio : {e}")
            return None
