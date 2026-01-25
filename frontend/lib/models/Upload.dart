
class Upload {

  final int songId;
  final String songName;
  final int songDuration;
  final bool private;
  final String date;
  final double predictedPopularity;


  const Upload(this.songId, this.songName, this.songDuration, this.private, this.date, this.predictedPopularity);

  factory Upload.fromJson(Map<String, dynamic> json) {
    return Upload(
      json['song_id'],
      json['song_name'],
      json['song_duration_ms'],
      json['private'],
      json['date'],
      json['analyze']['predicted_popularity'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
    };
  }

  String getFormatedDuration() {
    int totalSeconds = songDuration ~/ 1000;
    int minutes = totalSeconds ~/ 60;
    int seconds = totalSeconds % 60;

    String secondsStr = seconds.toString().padLeft(2, '0');

    return "${minutes}min$secondsStr";
  }
}