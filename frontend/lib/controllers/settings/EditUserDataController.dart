
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/User.dart';
import 'package:discover/services/AuthService.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/UserService.dart';
import 'package:flutter/cupertino.dart';

import '../../core/CustomNavigator.dart';
import '../../exceptions/RequestException.dart';

class EditUserDataController with ChangeNotifier {

  UserService userService;
  AuthService authService;
  EditUserDataController(this.userService, this.authService);

  User? user;

  final nameController = TextEditingController();
  final emailController = TextEditingController();

  Future<void> initData() async {
    try {
      user = await authService.recoverUser();
      nameController.text = user!.name;
      emailController.text = user!.email;
      notifyListeners();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (_) {
      DialogBuilder.appError();
    }
  }

  void submitForm(GlobalKey<FormState> formKey) async {

    if (!formKey.currentState!.validate()) {
      DialogBuilder.warning("The form is not valid", "Please check your inputs");
      return;
    }

    if (user == null) {
      DialogBuilder.error("Couldn't update your account", "We are missing some data about you. Please contact us.");
      return;
    }

    String name = nameController.text.trim();
    String email = emailController.text.trim();

    DialogBuilder.loading();

    try {
      await userService.updateUser(email, name);
      user = await authService.recoverUser();
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.back();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }
}