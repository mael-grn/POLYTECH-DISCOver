
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Song.dart';
import 'package:discover/services/UploadService.dart';
import 'package:discover/views/upload/UploadNewSongView.dart';
import 'package:flutter/cupertino.dart';

import '../exceptions/RequestException.dart';


class HomeController with ChangeNotifier {

  HomeController(this.uploadService);
  final Uploadservice uploadService;

  Song? song = null;
  List<String> trends = ["Aucune donnée."];

  Future<void> initData() async {
    trends = [
      "Say My Name - Destiny's Child",
      "Inspecteur gadget - Shuki Levy, Haim Saban et Jacques Cardona",
      "Axel F - Crazy Frog",
      "He’s a Pirate - Geoff Zanelli, Hans Zimmer et Klaus Badelt",
      "Zillertaler Bravourjodler - Musikantenstadl"
    ];
    try {
      song = await uploadService.getLastUploadedSongByUser();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (_) {
      DialogBuilder.appError();
    }
    notifyListeners();
  }

  void onUploadSongClicked() {
    CustomNavigator.pushFromRight(UploadNewSongView());
  }

  void onDiscoverSomeMusicCLicked() {
    DialogBuilder.warning("You're too fast", "This functionality has not been developed yet.");
  }
}