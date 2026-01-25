from app.models.song import Song

def song_to_features(song: Song) -> dict:
    return song.to_features_dict()
