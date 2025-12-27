
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/views/UploadView.dart';
import 'package:flutter/cupertino.dart';


class HomeController with ChangeNotifier {

  HomeController();

  Future<void> initData() async {

  }

  void onUploadSongClicked() {
    CustomNavigator.pushFromRight(Uploadview());
  }

  void onDiscoverSomeMusicCLicked() {
    DialogBuilder.warning("You're too fast", "This functionality has not been developed yet.");

  }
}