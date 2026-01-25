from app.models.song import Song

def song_to_features(song: Song) -> dict:
    """
    Récupère un dictionnaire des caractéristiques audio de la chanson.

    - song : instance de Song
    - retourne :
        - dict contenant toutes les caractéristiques audio via song.to_features_dict()
    """
    return song.to_features_dict()
