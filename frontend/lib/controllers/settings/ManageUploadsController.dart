
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/UploadService.dart';
import 'package:flutter/cupertino.dart';

import '../../core/CustomNavigator.dart';
import '../../exceptions/RequestException.dart';
import '../../views/upload/UploadNewSongView.dart';

class ManageUploadsController with ChangeNotifier {

  Uploadservice uploadService;
  ManageUploadsController(this.uploadService);

  List<Upload> userUploads = [];

  Future<void> initData() async {
    try {
      userUploads = await uploadService.getMyUploads();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      print(e)
;      DialogBuilder.appError();
    }
  }

  void onDeleteUploadPressed(int index) {
    DialogBuilder.warning("Sorry, you cannot do that right now", "The app is currently in very early development, and the functionality is not implemented yet");
  }

  void onAddUploadPressed() {
    CustomNavigator.pushFromRight(UploadNewSongView());
  }

}