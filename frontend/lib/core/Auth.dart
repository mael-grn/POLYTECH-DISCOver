import 'dart:convert';
import 'package:discover/exceptions/AuthException.dart';
import 'package:discover/utils/StorageUtils.dart';
import '../models/User.dart';

class Auth {
  static User? _connectedUser;

  static Future<User> getConnectedUser() async {
    if (_connectedUser != null) {
      return _connectedUser!;
    }

    final value = await StorageUtils.load("user");

    if (value.isNotEmpty) {
      _connectedUser = User.fromJson(jsonDecode(value));

      if (_connectedUser != null) {
        return _connectedUser!;
      }
    }

    throw AuthException();
  }

  static void setConnectedUser(User user) {
    _connectedUser = user;
    StorageUtils.save("user", JsonEncoder().convert(user.toJson()));
  }

  static void logout() {
    _connectedUser = null;
    StorageUtils.remove("token");
    StorageUtils.remove("user");
  }

  static Future<bool> isLoggedIn() async {
    try {
      await getConnectedUser();
      return true;
    } on AuthException catch (_) {
      return false;
    }
  }
}