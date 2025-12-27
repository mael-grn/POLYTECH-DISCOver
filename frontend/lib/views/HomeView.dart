
import 'package:discover/controllers/HomeController.dart';
import 'package:discover/core/theme/app_theme.dart';
import 'package:discover/widgets/ui/button_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomeView extends StatefulWidget {
  HomeView({super.key});

  @override
  State<HomeView> createState() => _HomeView();
}

class _HomeView extends State<HomeView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<HomeController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<HomeController>();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Image.asset(width: 500, height: 333, "images/team/mael-welcome.png"),
        SizedBox(
          height: 20,
        ),
        ButtonWidget(message: "Upload a song", icon: Icons.cloud_upload_rounded, onPressed: controller.onUploadSongClicked),
        SizedBox(
          height: 50,
        ),
        ButtonWidget(message: "Discover some music", icon: Icons.music_note, onPressed: controller.onDiscoverSomeMusicCLicked),
      ],
    );
  }
}