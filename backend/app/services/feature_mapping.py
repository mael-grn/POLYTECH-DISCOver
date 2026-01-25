from app.models.song import Song

# Transforme une chanson en dictionnaire contenant ses caractéristiques
def song_to_features(song: Song) -> dict:
    return song.to_features_dict()
