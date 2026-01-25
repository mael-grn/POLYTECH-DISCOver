
import 'package:discover/controllers/AccountController.dart';
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

import '../../widgets/ui/ButtonWidget.dart';


class UserDataView extends StatefulWidget {
  UserDataView({super.key});

  @override
  State<UserDataView> createState() => _UserDataView();
}

class _UserDataView extends State<UserDataView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ViewUserDataController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<ViewUserDataController>();

    return PageWidget(
        title: "My personal data",
        body: SingleChildScrollView(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  LordiconWidget("eye"),
                  SizedBox(height: 15,),
                  Text(
                    "Here is your personal data",
                    style: TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ContainerWidget(
                      controller.user == null ? Text("No user data") :
                      Column(
                        children: [
                          TextInfoWidget("Name", controller.user?.name ?? ""),
                          TextInfoWidget("Email", controller.user?.email ?? ""),
                        ],
                      )
                  ),
                  SizedBox(height: 20,),
                  ButtonWidget(
                    message: "Edit my data",
                    icon: Icons.loop,
                    onPressed: () => controller.onEditDataPressed(),
                  ),
                ]
            )
        )
    );
  }
}