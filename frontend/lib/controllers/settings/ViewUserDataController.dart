
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/User.dart';
import 'package:discover/services/AuthService.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/UserService.dart';
import 'package:flutter/cupertino.dart';

import '../../exceptions/RequestException.dart';

class ViewUserDataController with ChangeNotifier {

  AuthService authService;
  ViewUserDataController(this.authService);

  User? user;

  Future<void> initData() async {

    try {
      user = await authService.recoverUser();
      notifyListeners();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (_) {
      DialogBuilder.appError();
    }
  }

  void onEditDataPressed() {

  }
}