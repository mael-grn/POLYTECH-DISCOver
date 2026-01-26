import 'dart:convert';
import 'package:discover/models/Song.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/models/UploadedResult.dart';
import '../core/provider.dart';
import '../exceptions/RequestException.dart';

class SongService {
  Future<List<Song>> getSongs() async {
    final response = await Provider.sendRequest(route: '/songs', method: HttpMethod.GET);
    final Map<String, dynamic> data = jsonDecode(response);
    final List<dynamic> listData = data['items'];
    return listData.map((item) => Song.fromJson(item)).toList();
  }

  Future<List<Song>> searchSongs(String q) async {
    final response = await Provider.sendRequest(route: '/songs?q=$q', method: HttpMethod.GET);
    final Map<String, dynamic> data = jsonDecode(response);
    final List<dynamic> listData = data['items'];
    return listData.map((item) => Song.fromJson(item)).toList();
  }

  Future<Song> getSongById(int id) async {
    final response = await Provider.sendRequest(route: "/songs/$id", method: HttpMethod.GET);
    print(response);
    return Song.fromJson(jsonDecode(response));
  }

  Future<double?> getAnalyzeBySongId(int id) async {
    try {
      final response = await Provider.sendRequest(route: "/analyze/$id", method: HttpMethod.GET);
      final Map<String, dynamic> data = jsonDecode(response);
      return (data["popularity_probability"] ?? 0.0).toDouble();
    } on NetworkException catch (e) {
      if (e.networkError.code == 404) {
        return null;
      }
      rethrow;
    }
  }

  Future<UploadedResult> getAnalyzePreviewBySongId(int id) async {
    final response = await Provider.sendRequest(route: "/analyze/$id/preview", method: HttpMethod.GET);
    return UploadedResult.fromJson(jsonDecode(response));
  }

  Future<List<Song>> getHistory() async {
    final response = await Provider.sendRequest(route: '/history', method: HttpMethod.GET);
    final Map<String, dynamic> data = jsonDecode(response);
    final List<dynamic> listData = data['items'];
    List<Song> songs = [];
    for (var item in listData) {
      Song song = await getSongById(item['song_id']);
      songs.add(song);
    }
    return songs;
  }
}