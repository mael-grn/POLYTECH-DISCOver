import 'dart:convert';
import 'package:discover/core/Auth.dart';
import '../core/provider.dart';
import '../enums/NetworkErrorEnum.dart';
import '../exceptions/RequestException.dart';
import '../models/User.dart';
import '../utils/StorageUtils.dart';

class AuthService {

  Future<void> login(String email, String password) async {
    await Provider.sendRequest(route: "/auth/login", method: HttpMethod.POST, body: {
      "email": email,
      "password": password
    });
    final response = await Provider.sendRequest(route: "/auth/me", method: HttpMethod.GET);
    final data = jsonDecode(response);
    print(data);
    if (data['logged_in'] == false) throw NetworkException(NetworkErrorEnum.unauthorized);
    User user = User.fromJson(data['user']);
    Auth.setConnectedUser(user);
  }

  Future<void> logout() async {
    await Provider.sendRequest(route: "/auth/logout", method: HttpMethod.POST);
    StorageUtils.remove("token");
    Auth.logout();
  }

  Future<User> recoverUser() async {
    final response = await Provider.sendRequest(route: "/auth/me", method: HttpMethod.GET);
    final data = jsonDecode(response);
    if (data['logged_in'] == false) throw NetworkException(NetworkErrorEnum.unauthorized);
    User user = User.fromJson(data['user']);
    Auth.setConnectedUser(user);
    return user;
  }
}