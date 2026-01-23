import 'dart:convert';

import '../core/Auth.dart';
import '../core/provider.dart';
import '../models/User.dart';

class UserService {

  Future<void> createUser(String name, String email, String password) async {
    await Provider.sendRequest(route: "/users", method: HttpMethod.POST, body: {
      "name": name,
      "email": email,
      "password": password
    });
    final response = await Provider.sendRequest(route: "/users/me", method: HttpMethod.GET);
    User user = User.fromJson(jsonDecode(response));
    Auth.setConnectedUser(user);
  }

  Future<User> getMe() async {
    final response = await Provider.sendRequest(route: "/users/me", method: HttpMethod.GET);
    return User.fromJson(jsonDecode(response));
  }
}