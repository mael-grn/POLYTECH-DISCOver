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

  static const String _baseUrl = 'URL DE BASE API';

  static Future<String> sendRequestWithCookies({required HttpMethod method, required String route, Map<String, String>? headers, Object? body}) async {
    // Récupère les cookies pour l'URL
    final url = Uri.parse('$_baseUrl$route');
    final token = await StorageUtils.load("token");

    final cookieHeader = 'token=$token';
    // Ajoute les cookies dans les headers
    final requestHeaders = {
      ...?headers,
      'Cookie': cookieHeader,
      'Content-Type': 'application/json',
    };

    // Envoie la requête
    late http.Response response;
    switch (method) {
      case HttpMethod.GET:
        response = await _client.get(url, headers: requestHeaders);
        break;
      case HttpMethod.PUT:
        response = await _client.put(url, headers: requestHeaders, body: jsonEncode(body));
        break;
      case HttpMethod.PATCH:
        response = await _client.patch(url, headers: requestHeaders, body: jsonEncode(body));
        break;
      case HttpMethod.DELETE:
        response = await _client.delete(url, headers: requestHeaders);
        break;
      case HttpMethod.POST:
        response = await _client.post(url, headers: requestHeaders, body: jsonEncode(body));
        break;
    }

    if (response.statusCode.toString().startsWith('2')) {

      // Stocke les nouveaux cookies reçus
      final setCookie = response.headers['set-cookie'];
      if (setCookie != null) {
        StorageUtils.save('token', Cookie.fromSetCookieValue(setCookie).value);
      }
      return response.body;
    } else {
      throw NetworkException(NetworkErrorEnum.fromCode(response.statusCode));
    }
  }

  static Future<String> sendRequest({required HttpMethod method, required String route, Map<String, String>? headers, Object? body}) async {
    final url = Uri.parse('$_baseUrl$route');
    final requestHeaders = {
      ...?headers,
      'Content-Type': 'application/json',
    };
    // Envoie la requête
    late http.Response response;
    switch (method) {
      case HttpMethod.GET:
        response = await _client.get(url, headers: requestHeaders);
        break;
      case HttpMethod.PUT:
        response = await _client.put(url, headers: requestHeaders, body: jsonEncode(body));
        break;
      case HttpMethod.PATCH:
        response = await _client.patch(url, headers: requestHeaders, body: jsonEncode(body));
        break;
      case HttpMethod.DELETE:
        response = await _client.delete(url, headers: requestHeaders);
        break;
      case HttpMethod.POST:
        response = await _client.post(url, headers: requestHeaders, body: jsonEncode(body));
        break;
    }

    if (response.statusCode.toString().startsWith('2')) {
      return response.body;
    } else {
      throw NetworkException(NetworkErrorEnum.fromCode(response.statusCode));
    }
  }
}
