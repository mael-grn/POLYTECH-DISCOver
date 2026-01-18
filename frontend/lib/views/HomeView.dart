
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
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Image.asset(width: 300, height: 200, "images/music_white.png"),
        Text(
          'Ready for the next era of music ?',
          style: TextStyle(
            color: foregroundColor,
            fontSize: 30,
          ),
          textAlign: TextAlign.center,
        ),
        SizedBox(
          height: 30,
        ),
        ButtonWidget(message: "Browse new songs", icon: Icons.music_note, onPressed: controller.onDiscoverNewSongsClicked),

      ],
    );
  }
}