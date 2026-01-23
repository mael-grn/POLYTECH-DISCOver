import 'package:discover/controllers/HomeController.dart';
import 'package:discover/core/theme/app_theme.dart';
import 'package:discover/widgets/animations/scale_animation_widget.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/button_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../widgets/ui/lordicon_widget.dart';

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

    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          ContainerWidget(
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                LordiconWidget("doodle-music"),
                SizedBox(height: 10),
                Text(
                  "No song recently uploaded",
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),
                ButtonWidget(
                  message: "Upload a song",
                  icon: Icons.upload_rounded,
                  onPressed: controller.onUploadSongClicked,
                ),
              ],
            ),
          ),
          SizedBox(height: 20),

          ContainerWidget(
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  "Trends",
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                ),
                SizedBox(height: 20),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.trends.length,
                  itemBuilder: (context, index) {
                    return Column(
                      children: [
                        SizedBox(height: 20),
                        Row(
                          children: [
                            index == 0
                                ? LordiconWidget("one", size: 100)
                                : index == 1
                                ? LordiconWidget("two", size: 100)
                                : index == 2
                                ? LordiconWidget("three", size: 100)
                                : Text("$index - "),
                            SizedBox(width: 10),
                            Expanded(child: Text(controller.trends[index], style: TextStyle(fontWeight: index < 3 ? FontWeight.w600 : FontWeight.w400, fontSize: index < 3 ? 20 : 15))),
                          ],
                        ),
                      ],
                    );
                  },
                ),
                SizedBox(height: 20),
                ButtonWidget(
                  message: "Discover some music",
                  icon: Icons.arrow_forward_rounded,
                  iconOnRight: true,
                  onPressed: controller.onDiscoverSomeMusicCLicked,
                  backgroundColor: secondaryColor,
                ),
              ],
            ),
          ),
          SizedBox(height: 120,)
        ],
      ),
    );
  }
}
