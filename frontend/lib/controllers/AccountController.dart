
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/views/auth/LoginView.dart';
import 'package:discover/views/settings/ServerStatusView.dart';
import 'package:discover/views/settings/UserDataView.dart';
import 'package:flutter/cupertino.dart';

import '../core/Auth.dart';
import '../core/CustomNavigator.dart';
import '../models/User.dart';


class AccountController with ChangeNotifier {

  AccountController();

  bool isLoggedIn = false;
  User? user;

  Future<void> initData() async {
    isLoggedIn = await Auth.isLoggedIn();
    if (isLoggedIn) {
      user = await Auth.getConnectedUser();
    }
    notifyListeners();
  }

  void onLoginPressed() {
    CustomNavigator.pushFromRight(LoginView());
  }

  void onSeeServerStatusPressed() {
    CustomNavigator.pushFromRight(ServerStatusView());
  }

  void onDisplayPressed() {
    DialogBuilder.warning("Not so fast!", "This functionality is not implemented yet");
  }

  void onDevicesPressed() {
    DialogBuilder.warning("Not so fast!", "This functionality is not implemented yet");
  }

  void onAudioPressed() {
    DialogBuilder.warning("Not so fast!", "This functionality is not implemented yet");
  }

  void onManageUploadsPressed() {
    DialogBuilder.warning("Not so fast!", "This functionality is not implemented yet");
  }

  void onAboutPressed() {
    DialogBuilder.warning("Not so fast!", "This functionality is not implemented yet");
  }

  void onManageAccountPressed() {
    CustomNavigator.pushFromRight(UserDataView());
  }
  void onLogoutPressed() {
    Auth.logout();
    CustomNavigator.resetToHome();
  }
}