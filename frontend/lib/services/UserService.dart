import 'dart:convert';

import 'package:discover/enums/NetworkErrorEnum.dart';
import 'package:discover/exceptions/RequestException.dart';

import '../core/Auth.dart';
import '../core/provider.dart';
import '../models/User.dart';

class UserService {

  Future<void> createUser(String name, String email, String password) async {
    Provider.sendRequest(route: "/users", method: HttpMethod.POST, body: {
      "name": name,
      "email": email,
      "password": password
    });
  }

  Future<void> updateUser(String email, String name) async {
    await Provider.sendRequest(route: "/users/me", method: HttpMethod.PATCH, body: {
      "name": name,
      "email": email,
    });
    final response = await Provider.sendRequest(route: "/auth/me", method: HttpMethod.GET);
    final data = jsonDecode(response);
    if (data['logged_in'] == false) throw NetworkException(NetworkErrorEnum.networkAuthenticationRequired);
    User user = User.fromJson(data['user']);
    Auth.setConnectedUser(user);
  }
}