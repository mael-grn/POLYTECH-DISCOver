
import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/widgets/ui/Text_field_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../widgets/ui/PageWidget.dart';
import '../widgets/ui/TextInputWidget.dart';

class ExploreView extends StatefulWidget {
  ExploreView({super.key});

  @override
  State<ExploreView> createState() => _ExploreView();
}

class _ExploreView extends State<ExploreView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ExploreController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<ExploreController>();

    return Column(
      children: [
        TextInputWidget(
          controller: controller.searchQueryController,
          hint: "Artists, songs, ...",
          icon: Icons.search,
          big: true,
        ),
      ],
    );
  }
}