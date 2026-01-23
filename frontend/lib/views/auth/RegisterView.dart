import 'package:discover/controllers/SearchSongController.dart';
import 'package:discover/core/theme/app_theme.dart';
import 'package:discover/validators/userValidators.dart';
import 'package:discover/widgets/search/songListItemWidget.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../controllers/registerController.dart';
import '../../models/Song.dart';
import '../../widgets/ui/button_widget.dart';

class RegisterView extends StatefulWidget {
  RegisterView({super.key});
  final _formKey = GlobalKey<FormState>();

  @override
  State<RegisterView> createState() => _RegisterView();
}

class _RegisterView extends State<RegisterView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<RegisterController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<RegisterController>();

    return PageWidget(
        body: SingleChildScrollView(
          child: Column(
            children: [
              LordiconWidget("card"),
              SizedBox(height: 20,),
              Text(
                "Register",
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
                        controller: controller.nameController,
                        hint: "name",
                        icon: Icons.person,
                        validator: UserValidators.nameValidator,
                      ),
                      SizedBox(height: 10,),
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
                        message: "Register",
                        icon: Icons.add_rounded,
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
                message: "Login",
                icon: Icons.open_in_new,
                onPressed: controller.onLoginPressed,
              ),
            ],
          ),
        )
    );
  }
}
