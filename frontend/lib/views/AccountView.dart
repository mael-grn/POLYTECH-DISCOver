import 'package:discover/controllers/AccountController.dart';
import 'package:discover/core/Auth.dart';
import 'package:discover/core/theme/app_theme.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/ListItemButton.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../widgets/ui/ButtonWidget.dart';

class AccountView extends StatefulWidget {
  AccountView({super.key});

  @override
  State<AccountView> createState() => _AccountView();
}

class _AccountView extends State<AccountView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<AccountController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<AccountController>();

    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Column(
            children: [
              Image.asset(width: 200, height: 200, "images/DISCOver.png"),
              Text(
                controller.isLoggedIn
                    ? controller.user?.name ?? "Who are you?"
                    : "You are not logged in",
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                textAlign: TextAlign.center,
              ),
              if (!controller.isLoggedIn) SizedBox(height: 20),
              if (!controller.isLoggedIn) ButtonWidget(
                message: "Login",
                icon: Icons.login,
                onPressed: controller.onLoginPressed,
              ),
            ],
          ),

          SizedBox(height: 20),

          ContainerWidget(
            Column(
              children: [
                ListItemButton(
                  title: "Server status",
                  onPressed: controller.onSeeServerStatusPressed,
                  icon: Icons.network_check,
                ),
                if (controller.isLoggedIn) SizedBox(height: 10),
                if (controller.isLoggedIn) ListItemButton(
                  title: "User data",
                  onPressed: controller.onManageAccountPressed,
                  icon: Icons.person,
                ),
                if (controller.isLoggedIn) SizedBox(height: 10),
                if (controller.isLoggedIn) ListItemButton(
                  title: "Manage uploads",
                  onPressed: controller.onManageUploadsPressed,
                  icon: Icons.upload_rounded,
                ),
                SizedBox(height: 10),
                ListItemButton(
                  title: "Display",
                  onPressed: controller.onDisplayPressed,
                  icon: Icons.display_settings,
                ),
                SizedBox(height: 10),
                ListItemButton(
                  title: "Device",
                  onPressed: controller.onDevicesPressed,
                  icon: Icons.devices,
                ),
                SizedBox(height: 10),
                ListItemButton(
                  title: "Audio",
                  onPressed: controller.onAudioPressed,
                  icon: Icons.audiotrack,
                ),
                SizedBox(height: 10),
                ListItemButton(
                  title: "About",
                  onPressed: controller.onAboutPressed,
                  icon: Icons.question_mark,
                ),
                if (controller.isLoggedIn) SizedBox(height: 10),
                if (controller.isLoggedIn) ListItemButton(
                  bgColor: invalidColor,
                  title: "Logout",
                  onPressed: controller.onLogoutPressed,
                  icon: Icons.logout,
                ),
              ],
            ),
          ),

          SizedBox(height: 120),
        ],
      ),
    );
  }
}
