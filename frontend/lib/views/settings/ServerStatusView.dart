
import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/ServerStatusController.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/listItemButton.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../widgets/ui/button_widget.dart';


class ServerStatusView extends StatefulWidget {
  ServerStatusView({super.key});

  @override
  State<ServerStatusView> createState() => _ServerStatusView();
}

class _ServerStatusView extends State<ServerStatusView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ServerStatusController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<ServerStatusController>();

    return PageWidget(
      title: "Check Server Status",
        body: SingleChildScrollView(
          child: ContainerWidget(
              Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    LordiconWidget(
                      controller.serverHealthy ? "cloud-check" : "cloud-cross",
                      key: ValueKey(controller.serverHealthy),
                    ),
                    SizedBox(height: 15,),
                    Text(
                      controller.serverHealthy ? "Server is healthy" : "Could not connect to server",
                      style: TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(height: 20),
                    ButtonWidget(
                      message: "Try again",
                      icon: Icons.loop,
                      onPressed: () => controller.checkServerHealth(),
                    ),
                  ]
              )
          )
        )
    );
  }
}