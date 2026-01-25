
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/SongService.dart';
import 'package:discover/services/UploadService.dart';
import 'package:flutter/cupertino.dart';

import '../../core/CustomNavigator.dart';
import '../../exceptions/RequestException.dart';
import '../../models/Song.dart';
import '../../views/song/SongView.dart';
import '../../views/upload/UploadNewSongView.dart';

class ManageUploadsController with ChangeNotifier {

  Uploadservice uploadService;
  SongService songService;
  ManageUploadsController(this.uploadService, this.songService);

  List<Upload> userUploads = [];

  Future<void> initData() async {
    try {
      userUploads = await uploadService.getMyUploads();
      notifyListeners();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
;      DialogBuilder.appError();
    }
  }

  void onUploadPressed(int index) async {
    DialogBuilder.loading();
    try {
      Song song = await songService.getSongById(userUploads[index].songId);
      double? analyze = await songService.getAnalyzeBySongId(song.id);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.pushFromBottom(SongView(song, analyze));
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }  }

  void onAddUploadPressed() {
    CustomNavigator.pushFromRight(UploadNewSongView());
  }

}