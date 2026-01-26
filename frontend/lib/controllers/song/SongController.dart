
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/models/UploadedResult.dart';
import 'package:discover/services/SongService.dart';
import 'package:flutter/cupertino.dart';
import '../../exceptions/RequestException.dart';



class SongController with ChangeNotifier {

  SongController(this.songService);
  final SongService songService;

  UploadedResult? analyzePreview = null;

  Future<void> initData() async {
    analyzePreview = null;
    notifyListeners();
  }

  void onAnalyzePreviewPressed(int songId) async {
    DialogBuilder.loading();
    try {
      analyzePreview = await songService.getAnalyzePreviewBySongId(songId);
      DialogBuilder.closeCurrentDialog();
      notifyListeners();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }
}