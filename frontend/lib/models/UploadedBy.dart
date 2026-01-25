import 'Song.dart';
import 'User.dart';

class Uploadedby {

  final User user;
  final Song song;
  final bool private;
  final DateTime date;

  const Uploadedby(this.user, this.song, this.private, this.date);

  factory Uploadedby.fromJson(Map<String, dynamic> json) {
    return Uploadedby(
      User.fromJson(json['user']),
      Song.fromJson(json['song']),
      json['private'],
      json['date'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user': user.toJson(),
      'song': song.toJson(),
      'private' : private,
      'date': date,
    };
  }
}