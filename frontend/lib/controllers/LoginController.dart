
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/services/AuthService.dart';
import 'package:discover/services/UserService.dart';
import 'package:discover/views/auth/RegisterView.dart';
import 'package:flutter/cupertino.dart';
import '../exceptions/RequestException.dart';


class LoginController with ChangeNotifier {

  LoginController(this.authService);
  final AuthService authService;
  bool obscureTextPassword = true;

  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> initData() async {
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

    String email = emailController.text.trim();
    String password = passwordController.text.trim();

    DialogBuilder.loading();

    try {
      await authService.login(email, password);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.resetToHome();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }

  void onRegisterPressed() {
    CustomNavigator.pushReplacementFromRight(RegisterView());
  }
}
