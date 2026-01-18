
import 'package:discover/controllers/UploadController.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

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

    return Column(
      children: [
        Text(
          'Upload',

        ),
      ],
    );
  }
}