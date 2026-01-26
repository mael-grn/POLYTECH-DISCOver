from app.models.song import Song

def song_to_features(song: Song) -> dict:
     """
    Transforme un objet Song en dictionnaire de ses caractéristiques audio.

    - song : instance de Song dont on veut extraire les caractéristiques
    - retourne :
        - dict contenant les caractéristiques audio suivantes :
            - song_duration_ms
            - acousticness
            - danceability
            - energy
            - instrumentalness
            - key
            - liveness
            - loudness
            - audio_mode
            - speechiness
            - tempo
            - time_signature
            - audio_valence
    """
    return {
        "song_duration_ms": song.song_duration_ms,
        "acousticness": song.acousticness,
        "danceability": song.danceability,
        "energy": song.energy,
        "instrumentalness": song.instrumentalness,
        "key": song.key,
        "liveness": song.liveness,
        "loudness": song.loudness,
        "audio_mode": song.audio_mode,
        "speechiness": song.speechiness,
        "tempo": song.tempo,
        "time_signature": song.time_signature,
        "audio_valence": song.audio_valence,
    }
