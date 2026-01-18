import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/PersonneExemple.dart';
import 'package:discover/services/PersonneExempleService.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

import '../exceptions/RequestException.dart';

class GestionPersonnExempleController with ChangeNotifier {

  final PersonneExampleService personneExampleService;
  final prenomController = TextEditingController();
  PersonneExemple personneExemple = PersonneExemple(-1, "", "");

  GestionPersonnExempleController(this.personneExampleService);

  Future<void> initData() async {

    DialogBuilder.loading();

    try {
      personneExemple = await personneExampleService.recupererPersonne();

      DialogBuilder.closeCurrentDialog();
      notifyListeners();

    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);

    } catch (_) {
      DialogBuilder.appError();
    }
  }

  Future<void> modifierPrenom(GlobalKey<FormState> formKey) async {
    if (!formKey.currentState!.validate()) {
      return;
    }

    DialogBuilder.loading();

    HapticFeedback.mediumImpact();

    String nouveauPrenom = prenomController.text;

    try {
      personneExemple = await personneExampleService.modifierPrenom(personneExemple.id, nouveauPrenom);

      DialogBuilder.closeCurrentDialog();
      DialogBuilder.success("Bravo !", "Vous avez réussi à modifier le prénom.");
      notifyListeners();

    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);

    } catch (_) {
      DialogBuilder.appError();
    }
  }
}