import 'dart:async';
import 'dart:convert';
import 'package:cookie_jar/cookie_jar.dart';
import 'package:http/http.dart' as http;
import '../enums/NetworkErrorEnum.dart';
import '../exceptions/RequestException.dart';
import '../utils/StorageUtils.dart';

class ProviderResponse {
  final int statusCode;
  final Map<String, dynamic> data;

  ProviderResponse(this.statusCode, this.data);
}

enum HttpMethod { GET, POST, PUT, DELETE, PATCH }

class Provider {
  static final _client = http.Client();
  static final _cookieJar = CookieJar();

  static const String _baseUrl = 'http://10.151.221.189:5000/api';

  //static const String _baseUrl = 'http://localhost:5000/api';

  static Future<String> sendRequest({
    required HttpMethod method,
    required String route,
    Map<String, String>? headers,
    Object? body,
  }) async {
    final url = Uri.parse('$_baseUrl$route');
    final tokenExists = await StorageUtils.itemExists("token");
    final token = await StorageUtils.load("token");
    Map<String, String> requestHeaders;
    if (tokenExists) {
      requestHeaders = {
        ...?headers,
        'Cookie': 'access_token=$token',
        'Content-Type': 'application/json',
      };
    } else {
      requestHeaders = {...?headers, 'Content-Type': 'application/json'};
    }
    // Envoie la requête
    late http.Response response;
    switch (method) {
      case HttpMethod.GET:
        response = await _client.get(url, headers: requestHeaders);
        break;
      case HttpMethod.PUT:
        response = await _client.put(
          url,
          headers: requestHeaders,
          body: jsonEncode(body),
        );
        break;
      case HttpMethod.PATCH:
        response = await _client.patch(
          url,
          headers: requestHeaders,
          body: jsonEncode(body),
        );
        break;
      case HttpMethod.DELETE:
        response = await _client.delete(url, headers: requestHeaders);
        break;
      case HttpMethod.POST:
        response = await _client.post(
          url,
          headers: requestHeaders,
          body: jsonEncode(body),
        );
        break;
    }

    if (response.statusCode.toString().startsWith('2')) {
      final setCookie = response.headers['set-cookie'];
      if (setCookie != null) {
        String token = setCookie.split(';').first.split('=').last;
        StorageUtils.save('token', token);
      }
      return response.body;
    } else {
      throw NetworkException(NetworkErrorEnum.fromCode(response.statusCode));
    }
  }

  static Future<String> sendMultipartRequest({
    required String route,
    required String filePath,
    String fileKey = 'file', // Le nom du champ attendu par votre API
    Map<String, String>? fields, // Pour envoyer d'autres données texte si besoin
  }) async {
    final url = Uri.parse('$_baseUrl$route');
    final token = await StorageUtils.load("token");

    // 1. Créer la requête Multipart
    var request = http.MultipartRequest('POST', url);

    // 2. Ajouter le token dans les headers (comme dans votre méthode standard)
    if (token != null) {
      request.headers['Cookie'] = 'access_token=$token';
    }

    // 3. Ajouter le fichier
    request.files.add(await http.MultipartFile.fromPath(
      fileKey,
      filePath,
    ));

    // 4. Ajouter d'éventuels champs texte supplémentaires
    if (fields != null) {
      request.fields.addAll(fields);
    }

    // 5. Envoyer la requête
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    // 6. Gérer la réponse (même logique que votre méthode existante)
    if (response.statusCode.toString().startsWith('2')) {
      return response.body;
    } else {
      throw NetworkException(NetworkErrorEnum.fromCode(response.statusCode));
    }
  }
}
