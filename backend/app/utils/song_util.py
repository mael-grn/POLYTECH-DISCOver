from app.models.song import Song

# Fonction renvoyant un dictionnaire basé sur les caractéristiques d'une chanson
def song_to_features(song: Song) -> dict:
    # Retourne un dictionnaire basé sur les caractéristiques d'une chanson
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
