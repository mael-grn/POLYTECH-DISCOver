
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Song.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/services/SongService.dart';
import 'package:discover/services/UploadService.dart';
import 'package:discover/views/upload/UploadNewSongView.dart';
import 'package:flutter/cupertino.dart';

import '../enums/NetworkErrorEnum.dart';
import '../exceptions/RequestException.dart';
import '../views/song/SongView.dart';


class HomeController with ChangeNotifier {

  HomeController(this.uploadService, this.songService);
  final Uploadservice uploadService;
  final SongService songService;

  Upload? upload = null;
  List<Song> trends = [];

  Future<void> initData() async {
    try {
      trends = await songService.getSongs();
      final uploadLst = await uploadService.getMyUploads();
      upload = uploadLst.isNotEmpty ? uploadLst.first : null;
    } on NetworkException catch (e) {
      if (e.networkError != NetworkErrorEnum.unauthorized) {
        DialogBuilder.networkError(e.networkError);
      }
    } catch (e) {
      DialogBuilder.appError();
    }
    notifyListeners();
  }

  void onUploadSongClicked() {
    CustomNavigator.pushFromRight(UploadNewSongView());
  }

  void onSongItemPressed(int index) async {
    DialogBuilder.loading();
    try {
      Song song = await songService.getSongById(trends[index].id);
      double? analyze = await songService.getAnalyzeBySongId(song.id);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.pushFromBottom(SongView(song, analyze));
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }

  void onDiscoverSomeMusicCLicked() {
    DialogBuilder.warning("You're too fast", "This functionality has not been developed yet.");
  }
}