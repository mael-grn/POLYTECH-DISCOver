
class Song {

  final int id;
  final String name;
  final String artist;
  final String album;
  final int annee;
  final String genre;
  final int duration; // En millisecondes
  final bool explicite;
  final double danceability;
  final double energy;
  final int key;
  final double loudness;
  final int mode;
  final double speechiness;
  final double acousticness;
  final double instrumentalness;
  final double liveness;
  final double valence;
  final double tempo;
  final int timeSignature;
  final bool isInDataset;


  const Song(this.id, this.name, this.artist, this.album, this.annee, this.genre, this.duration, this.explicite, this.danceability, this.energy, this.key, this.loudness, this.mode, this.speechiness, this.acousticness, this.instrumentalness, this.liveness, this.valence, this.tempo, this.timeSignature, this.isInDataset);

  factory Song.fromJson(Map<String, dynamic> json) {
    return Song(
      json['song_id'],
      json['song_name'],
      json['artist'],
      json['album'],
      json['annee'],
      json['genre'],
      json['song_duration_ms'],
      json['explicite'],
      json['danceability'],
      json['energy'],
      json['key'],
      json['loudness'],
      json['mode'],
      json['speechiness'],
      json['acousticness'],
      json['instrumentalness'],
      json['liveness'],
      json['valence'],
      json['tempo'],
      json['time_signature'],
      json['isInDataset'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'song_id': id,
      'song_name': name,
      'artist': artist,
      'album': album,
      'annee': annee,
      'genre': genre,
      'song_duration_ms': duration,
      'explicite': explicite,
      'danceability': danceability,
      'energy': energy,
      'key': key,
      'loudness': loudness,
      'mode': mode,
      'speechiness': speechiness,
      'acousticness': acousticness,
      'instrumentalness': instrumentalness,
      'liveness': liveness,
      'valence': valence,
      'tempo': tempo,
      'time_signature': timeSignature,
      'isInDataset': isInDataset,
    };
  }
}