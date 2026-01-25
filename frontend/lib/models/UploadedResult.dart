
class UploadedResult {

  final int songId;
  final String songName;
  final double predictedPopularity;
  final bool private;

  const UploadedResult(this.songId, this.songName, this.predictedPopularity, this.private);

  factory UploadedResult.fromJson(Map<String, dynamic> json) {
    return UploadedResult(
      json['song_id'],
      json['song_name'],  
      json['predicted_popularity'],
      json['private'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
    };
  }
}