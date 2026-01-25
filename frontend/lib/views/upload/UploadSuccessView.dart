import 'package:discover/controllers/upload/UploadController.dart';
import 'package:discover/controllers/upload/UploadSuccessController.dart';
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/views/GlobalLayout.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/ButtonWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../models/UploadedResult.dart';
import '../../widgets/ui/PageWidget.dart';

class Uploadsuccessview extends StatefulWidget {
  Uploadsuccessview(this.uploadData, {super.key});
  UploadedResult uploadData;

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
        body: Column(
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

              ContainerWidget(
                  Column(
                    children: [
                      LordiconWidget("trends"),
                      SizedBox(height: 10),
                      Text(
                        "The predicted popularity is:",
                        style: TextStyle(fontWeight: FontWeight.w300, fontSize: 18),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 5),
                      Text(
                        "${widget.uploadData.predictedPopularity}%",
                        style: TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  )
              ),

              SizedBox(height: 20,),

              ButtonWidget(message: "Back to home page", icon: Icons.check, onPressed: controller.goBackHome),
            ]
        ),
    );
  }
}
