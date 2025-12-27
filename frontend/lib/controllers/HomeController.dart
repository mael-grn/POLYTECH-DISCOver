
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/views/UploadView.dart';
import 'package:flutter/cupertino.dart';


class HomeController with ChangeNotifier {

  HomeController();

  List<String> trends = ["Aucune donnée."];

  Future<void> initData() async {
    trends = [
      "Say My Name - Destiny's Child",
      "Inspecteur gadget - Shuki Levy, Haim Saban et Jacques Cardona",
      "Axel F - Crazy Frog",
      "He’s a Pirate - Geoff Zanelli, Hans Zimmer et Klaus Badelt",
      "Zillertaler Bravourjodler - Musikantenstadl"
    ];
  }

  void onUploadSongClicked() {
    CustomNavigator.pushFromRight(Uploadview());
  }

  void onDiscoverSomeMusicCLicked() {
    DialogBuilder.warning("You're too fast", "This functionality has not been developed yet.");
  }
}