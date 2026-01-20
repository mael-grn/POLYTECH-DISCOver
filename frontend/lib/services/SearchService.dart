import '../core/provider.dart';
import '../models/Song.dart';
import 'dart:convert';

class SearchService {

  static Future<List<Song>> searchSongs(String query) async {
    print("🔥 searchSongs() CALLED");
    // On ajoute la query directement dans l'URL
    final encodedQuery = Uri.encodeQueryComponent(query);
    final responseBody = await Provider.sendRequest(
      method: HttpMethod.GET,
      route: '/songs/search?q=$encodedQuery',
    );
    
    print("QUERY: $query");
    print("API RESPONSE RAW: $responseBody");

    final List<dynamic> jsonData = jsonDecode(responseBody);
    return jsonData.map((e) => Song.fromJson(e)).toList();
  }

}
