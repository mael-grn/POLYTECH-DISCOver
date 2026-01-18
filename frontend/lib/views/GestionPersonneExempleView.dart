
import 'package:discover/controllers/gestionPersonneExempleController.dart';
import 'package:discover/utils/ValidatorUtils.dart';
import 'package:discover/widgets/ui/Text_field_widget.dart';
import 'package:discover/widgets/ui/text_info_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme/app_theme.dart';
import '../widgets/ui/button_widget.dart';

class GestionPersonneExempleView extends StatefulWidget {
  GestionPersonneExempleView({super.key});
  final _formKey = GlobalKey<FormState>();

  @override
  State<GestionPersonneExempleView> createState() => _GestionPersonneExempleViewState();
}

class _GestionPersonneExempleViewState extends State<GestionPersonneExempleView> {

  @override
  void initState() {
    super.initState();
    final controller = Provider.of<GestionPersonnExempleController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<GestionPersonnExempleController>();
    
    return Scaffold(
      appBar: AppBar(
          elevation: 0,
          title: Text(
              "Gestion d'une personne exemple"
          ),
          scrolledUnderElevation: 10.0,
          surfaceTintColor: backgroundVariantColor,
          backgroundColor: backgroundColor
      ),
      body: Column(
        children: [
          TextInfoWidget("Prenom", controller.personneExemple.prenom),
          TextInfoWidget("Nom", controller.personneExemple.nom),

          SizedBox(height: 20),

          Form(
            key: widget._formKey,
            child: TextFieldWidget(
              controller: controller.prenomController,
              labelText: "Nouveau prénom",
              validator: ValidatorUtils.checkPrenomFormat,
            )
          ),

          SizedBox(height: 20),

          ButtonWidget(
            onPressed: () {
              controller.modifierPrenom(widget._formKey);
            },
            message: "Valider",
            icon: Icons.save,
          ),
        ],
      ),
    );
  }
}