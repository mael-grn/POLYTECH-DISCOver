// import 'dart:ffi';

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
      json['song_id'] ?? 0,
      json['song_name'] ?? '',
      json['artist'] ?? 'Unknown',
      json['album'] ?? 'Unknown',
      json['annee'] ?? 0,
      json['genre'] ?? 'Unknown',
      json['song_duration_ms'] ?? 0,
      json['explicite'] ?? false,
      (json['danceability'] ?? 0.0).toDouble(),
      (json['energy'] ?? 0.0).toDouble(),
      json['key'] ?? 0,
      (json['loudness'] ?? 0.0).toDouble(),
      json['mode'] ?? 0,
      (json['speechiness'] ?? 0.0).toDouble(),
      (json['acousticness'] ?? 0.0).toDouble(),
      (json['instrumentalness'] ?? 0.0).toDouble(),
      (json['liveness'] ?? 0.0).toDouble(),
      (json['valence'] ?? 0.0).toDouble(),
      (json['tempo'] ?? 0.0).toDouble(),
      json['time_signature'] ?? 4,
      json['isInDataset'] ?? true,
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