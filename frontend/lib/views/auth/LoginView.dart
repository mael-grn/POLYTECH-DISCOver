import 'package:discover/controllers/SearchSongController.dart';
import 'package:discover/validators/userValidators.dart';
import 'package:discover/widgets/search/songListItemWidget.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../controllers/LoginController.dart';
import '../../controllers/registerController.dart';
import '../../core/theme/app_theme.dart';
import '../../models/Song.dart';
import '../../widgets/ui/button_widget.dart';

class LoginView extends StatefulWidget {
  LoginView({super.key});
  final _formKey = GlobalKey<FormState>();

  @override
  State<LoginView> createState() => _LoginView();
}

class _LoginView extends State<LoginView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<LoginController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<LoginController>();

    return PageWidget(
        body: SingleChildScrollView(
          child: Column(
            children: [
              LordiconWidget("protection"),
              SizedBox(height: 20,),
              Text(
                "Login",
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 30),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 20),

              ContainerWidget(
                  Form(
                    key: widget._formKey,

                    child: Column(
                      children: [
                        TextInputWidget(
                          controller: controller.emailController,
                          hint: "email",
                          icon: Icons.email,
                          validator: UserValidators.emailValidator,
                        ),
                        SizedBox(height: 10,),
                        TextInputWidget(
                          obscureText: true,
                          controller: controller.passwordController,
                          hint: "password",
                          icon: controller.obscureTextPassword ? Icons.visibility : Icons.visibility_off,
                          onIconClick: controller.toggleObscureTextPassword,
                          validator: UserValidators.passwordValidator,
                        ),
                        SizedBox(height: 20,),
                        ButtonWidget(
                          message: "Login",
                          icon: Icons.lock,
                          onPressed: () {
                            controller.submitForm(widget._formKey);
                          },
                        ),
                      ],
                    ),
                  )
              ),
              SizedBox(height: 30,),
              ButtonWidget(
                backgroundColor: secondaryColor,
                message: "Register",
                icon: Icons.open_in_new,
                onPressed: controller.onRegisterPressed,
              ),
            ],
          ),
        )
    );
  }
}
