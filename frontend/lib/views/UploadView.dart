import 'package:discover/controllers/UploadController.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/button_widget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:lordicon/lordicon.dart';
import 'package:provider/provider.dart';

import '../core/theme/app_theme.dart';
import '../widgets/ui/PageWidget.dart';

class Uploadview extends StatefulWidget {
  Uploadview({super.key});

  @override
  State<Uploadview> createState() => _Uploadview();
}

class _Uploadview extends State<Uploadview> {
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
          child: ContainerWidget(
            Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(height: 35),
                  LordiconWidget("cloud-plus", loop: controller.isUploading,),
                  SizedBox(height: 20),
                  Text(
                    "Select a file to start uploading",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ButtonWidget(tag: "upload-song-btn", message: "Select a file", icon: Icons.insert_drive_file, onPressed: controller.insertFile),


                ]
            ),
          )
        )
    );
  }
}
