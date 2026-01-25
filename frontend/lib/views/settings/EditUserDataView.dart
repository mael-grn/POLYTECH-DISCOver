
import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/settings/EditUserDataController.dart';
import 'package:discover/controllers/settings/ServerStatusController.dart';
import 'package:discover/controllers/settings/ViewUserDataController.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/ListItemButton.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:discover/widgets/ui/TextInfoWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../validators/UserValidators.dart';
import '../../widgets/ui/ButtonWidget.dart';
import '../../widgets/ui/TextInputWidget.dart';


class EditUserDataView extends StatefulWidget {
  EditUserDataView({super.key});
  final _formKey = GlobalKey<FormState>();

  @override
  State<EditUserDataView> createState() => _EditUserDataView();
}

class _EditUserDataView extends State<EditUserDataView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<EditUserDataController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<EditUserDataController>();

    return PageWidget(
        title: "Edit my data",
        body: SingleChildScrollView(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  LordiconWidget("envelope"),
                  SizedBox(height: 15,),
                  Text(
                    "Edit your personal data",
                    style: TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ContainerWidget(
                      controller.user == null ? Text("No user data") :
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
                            ],
                          )
                      )
                  ),
                  SizedBox(height: 20,),
                  ButtonWidget(
                    message: "Confirm",
                    icon: Icons.check,
                    onPressed: () => controller.submitForm(widget._formKey),
                  ),
                ]
            )
        )
    );
  }
}