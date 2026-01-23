import 'dart:convert';
import 'package:discover/exceptions/AuthException.dart';
import 'package:discover/utils/StorageUtils.dart';
import '../models/User.dart';

class Auth {
  static User? _connectedUser;

  static getConnectedUser() {
    if (_connectedUser == null) {
      StorageUtils.load("user").then((value) {
        if (value.isNotEmpty) {
          _connectedUser = User.fromJson(JsonDecoder().convert(value));
        } else {
          throw AuthException();
        }
      });
    }
    return _connectedUser;
  }

  static setConnectedUser(User user) {
    _connectedUser = user;
    StorageUtils.save("user", JsonEncoder().convert(user.toJson()));
  }

  static void logout() {
    _connectedUser = null;
    StorageUtils.remove("user");
  }

  static isLoggedIn() {
    try {
      getConnectedUser();
      return true;
    } catch (e) {
      return false;
    }
  }
}