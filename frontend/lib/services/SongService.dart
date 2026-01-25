import 'dart:convert';
import 'package:discover/models/Song.dart';
import '../core/provider.dart';

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
    return Song.fromJson(jsonDecode(response));
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