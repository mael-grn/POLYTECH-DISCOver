import 'package:discover/controllers/upload/UploadController.dart';
import 'package:discover/controllers/upload/UploadSuccessController.dart';
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/views/GlobalLayout.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/button_widget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../widgets/ui/PageWidget.dart';

class Uploadsuccessview extends StatefulWidget {
  Uploadsuccessview({super.key});

  @override
  State<Uploadsuccessview> createState() => _Uploadsuccessview();
}

class _Uploadsuccessview extends State<Uploadsuccessview> {

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<UploadSuccessController>();



    return PageWidget(
      showBackBtn: false,
        title: "Song successfully uploaded",
        body: Center(
            child: ContainerWidget(
              Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(height: 35),
                    LordiconWidget("check"),
                    SizedBox(height: 20),
                    Text(
                      "You have successfully imported your song into the library",
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 20),

                    ButtonWidget(message: "Back to home page", icon: Icons.insert_drive_file, onPressed: controller.goBackHome),
                  ]
              ),
            )
        )
    );
  }
}
