
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/services/UserService.dart';
import 'package:discover/views/auth/LoginView.dart';
import 'package:flutter/cupertino.dart';
import '../../exceptions/RequestException.dart';


class RegisterController with ChangeNotifier {

  RegisterController(this.userService);
  final UserService userService;

  bool obscureTextPassword = true;

  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> initData() async {
  }

  void onLoginPressed() {
    CustomNavigator.pushReplacementFromRight(LoginView());
  }

  void toggleObscureTextPassword() {
    obscureTextPassword = !obscureTextPassword;
    notifyListeners();
  }

  void submitForm(GlobalKey<FormState> formKey) async {

    if (!formKey.currentState!.validate()) {
      DialogBuilder.warning("The form is not valid", "Please check your inputs");
      return;
    }

    String name = nameController.text.trim();
    String email = emailController.text.trim();
    String password = passwordController.text.trim();

    DialogBuilder.loading();

    try {
      await userService.createUser(name, email, password);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.resetToHome();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }
}