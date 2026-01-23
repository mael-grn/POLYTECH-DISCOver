
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/views/auth/LoginView.dart';
import 'package:discover/views/settings/ServerStatusView.dart';
import 'package:flutter/cupertino.dart';

import '../core/Auth.dart';
import '../core/CustomNavigator.dart';


class AccountController with ChangeNotifier {

  AccountController();

  bool isLoggedIn = false;

  Future<void> initData() async {
    isLoggedIn = await Auth.isLoggedIn();
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
}