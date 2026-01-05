
import 'package:flutter/cupertino.dart';


class UploadController with ChangeNotifier {

  bool isUploading = false;

  UploadController();

  Future<void> initData() async {

  }

  void insertFile() {
    isUploading = true;
    notifyListeners();

  }
}