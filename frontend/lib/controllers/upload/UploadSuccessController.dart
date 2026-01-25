import 'package:flutter/cupertino.dart';
import '../../core/CustomNavigator.dart';
import '../../views/GlobalLayout.dart';


class UploadSuccessController with ChangeNotifier {



  UploadSuccessController();

  Future<void> initData() async {

  }

  void goBackHome() {
    CustomNavigator.resetToHome();
  }

}