
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:flutter/cupertino.dart';


class HomeController with ChangeNotifier {

  HomeController();

  Future<void> initData() async {

  }

  void onDiscoverNewSongsClicked() {
    DialogBuilder.warning("You're too fast", "This functionality has not been developed yet.");
  }
}