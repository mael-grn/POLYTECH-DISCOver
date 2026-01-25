import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/settings/ServerStatusController.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/ListItemButton.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:discover/widgets/uploads/UploadListItem.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../controllers/settings/ManageUploadsController.dart';
import '../../widgets/ui/ButtonWidget.dart';

class ManageUploadsView extends StatefulWidget {
  ManageUploadsView({super.key});

  @override
  State<ManageUploadsView> createState() => _ManageUploadsView();
}

class _ManageUploadsView extends State<ManageUploadsView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ManageUploadsController>(
      context,
      listen: false,
    );
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<ManageUploadsController>();

    return PageWidget(
      title: "Manage uploads",
      body: SingleChildScrollView(
        child: Column(
          children: [
            LordiconWidget("cloud-check"),
            SizedBox(height: 10),
            Text(
              "Manage your uploads",
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
              textAlign: TextAlign.center,
            ),
            if (controller.userUploads.isNotEmpty) SizedBox(height: 10),
            if (controller.userUploads.isNotEmpty)ButtonWidget(message: "Upload another song", icon: Icons.upload, onPressed: controller.onAddUploadPressed),
            SizedBox(height: 20),
            ContainerWidget(
              controller.userUploads.isEmpty
                  ? Column(
                  children: [
                    LordiconWidget("search", size: 100,),
                    SizedBox(height: 10),
                    Text(
                      "You have no uploads yet.",
                      style: TextStyle(fontWeight: FontWeight.w500, fontSize: 20),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 10),
                    ButtonWidget(message: "Start uploading", icon: Icons.upload, onPressed: controller.onAddUploadPressed)
                  ]
              )
                  : ListView.separated(
                separatorBuilder: (context, index) =>
                    SizedBox(height: 10),
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: controller.userUploads.length,
                itemBuilder: (context, index) {
                  final Upload upload = controller.userUploads[index];
                  return UploadListItemWidget(
                    upload: upload,
                    onItemPressed: () =>
                        controller.onUploadPressed(index),                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
