import 'dart:convert';
import 'package:discover/core/Auth.dart';
import '../core/provider.dart';
import '../models/User.dart';

class AuthService {

  Future<void> login(String email, String password) async {
    await Provider.sendRequest(route: "/login", method: HttpMethod.POST, body: {
      "email": email,
      "password": password
    });
    final response = await Provider.sendRequest(route: "/users/me", method: HttpMethod.GET);
    User user = User.fromJson(jsonDecode(response));
    Auth.setConnectedUser(user);
  }
}