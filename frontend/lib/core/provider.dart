import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../enums/NetworkErrorEnum.dart';
import '../exceptions/RequestException.dart';

class ProviderResponse {
  final int statusCode;
  final Map<String, dynamic> data;
  ProviderResponse(this.statusCode, this.data);
}

enum HttpMethod { GET, POST, PUT, DELETE, PATCH }

class Provider {

  static final _client = http.Client();

  static const String _baseUrl = 'URL DE BASE API';

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
