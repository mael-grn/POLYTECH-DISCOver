import 'package:discover/controllers/upload/UploadController.dart';
import 'package:discover/core/theme/app_theme.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/ButtonWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../widgets/ui/PageWidget.dart';

class UploadNewSongView extends StatefulWidget {
  UploadNewSongView({super.key});

  @override
  State<UploadNewSongView> createState() => _UploadNewSongView();
}

class _UploadNewSongView extends State<UploadNewSongView> {
  @override
  void initState() {
    super.initState();

    final controller = Provider.of<UploadController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<UploadController>();

    return PageWidget(
      title: "Upload a song",
      body: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ContainerWidget(
              Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(height: 35),
                  LordiconWidget("cloud-plus"),
                  SizedBox(height: 20),
                  Text(
                    controller.selectedFileName != null
                        ? controller.selectedFileName!
                        : "Select a file to start uploading",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text("Private"),
                      SizedBox(width: 10),
                      Checkbox(value: controller.private, onChanged: controller.setPrivate),
                    ],
                  ),
                  SizedBox(height: 20),
                  ButtonWidget(
                    message: "Select a file",
                    icon: Icons.insert_drive_file,
                    onPressed: controller.selectFile,
                  ),
                ],
              ),
            ),
            SizedBox(height: 20,),
            if (controller.hasSelectedFile())
              ButtonWidget(
                message: "Upload",
                icon: Icons.upload,
                onPressed: controller.uploadSelectedFile,
                backgroundColor: secondaryColor,
                padding: const EdgeInsets.symmetric(vertical: 25, horizontal: 40),
              ),
          ],
        ),
      ),
    );
  }
}
