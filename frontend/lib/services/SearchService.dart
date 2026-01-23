import '../core/provider.dart';
import '../models/Song.dart';
import 'dart:convert';

class SearchService {

  static Future<List<Song>> searchSongs(String query) async {
    print("debut");
    final encodedQuery = Uri.encodeQueryComponent(query);
    print("envoyé");
    final responseBody = await Provider.sendRequest(
      method: HttpMethod.GET,
      route: '/songs/search?q=$encodedQuery',
    );
    print("recu");


    final List<dynamic> jsonData = jsonDecode(responseBody);
    return jsonData.map((e) => Song.fromJson(e)).toList();
  }
}
