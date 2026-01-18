
import 'package:discover/controllers/AccountController.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AccountView extends StatefulWidget {
  AccountView({super.key});

  @override
  State<AccountView> createState() => _AccountView();
}

class _AccountView extends State<AccountView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<AccountController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<AccountController>();

    return Column(
      children: [
        Text(
          'Mon compte',

        ),
      ],
    );
  }
}