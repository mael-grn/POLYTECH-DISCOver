import 'package:discover/models/Song.dart';
import 'User.dart';

class History {
  final Map<DateTime, Song> songs;
  final User user;

  const History(this.user, this.songs);

  factory History.fromJson(Map<String, dynamic> json) {
    return History(
      User.fromJson(json['user']),
      json['songs'], // @todo Mettre a jour pour la conversion d'une liste
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user': user.toJson(),
      'songs': songs, // @todo Mettre a jour pour la conversion d'une liste
    };
  }
}