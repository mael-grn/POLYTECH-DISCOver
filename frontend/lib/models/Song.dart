
class Song {

  final int id;
  final String name;
  final int duration; // En millisecondes
  final double danceability;
  final double energy;
  final int key;
  final double loudness;
  final double acousticness;
  final double instrumentalness;
  final double liveness;
  final bool isInDataset;


  const Song(this.id, this.name, this.duration, this.danceability, this.energy, this.key, this.loudness, this.acousticness, this.instrumentalness, this.liveness, this.isInDataset);

  factory Song.fromJson(Map<String, dynamic> json) {
    return Song(
      json['song_id'] ?? -1,
      json['song_name'] ?? '',
      json['song_duration_ms'] ?? 0,
      (json['danceability'] ?? 0.0).toDouble(),
      (json['energy'] ?? 0.0).toDouble(),
      json['key'] ?? 0,
      (json['loudness'] ?? 0.0).toDouble(),
      (json['acousticness'] ?? 0.0).toDouble(),
      (json['instrumentalness'] ?? 0.0).toDouble(),
      (json['liveness'] ?? 0.0).toDouble(),
      json['upload'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'song_id': id,
      'song_name': name,
      'song_duration_ms': duration,
      'danceability': danceability,
      'energy': energy,
      'key': key,
      'loudness': loudness,
      'acousticness': acousticness,
      'instrumentalness': instrumentalness,
      'liveness': liveness,
      'upload': isInDataset,
    };
  }

  String getFormatedDuration() {
    int totalSeconds = duration ~/ 1000;
    int minutes = totalSeconds ~/ 60;
    int seconds = totalSeconds % 60;

    String secondsStr = seconds.toString().padLeft(2, '0');

    return "${minutes}min$secondsStr";
  }
}