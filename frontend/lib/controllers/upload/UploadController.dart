
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/views/HomeView.dart';
import 'package:discover/views/upload/UploadSuccessView.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/cupertino.dart';

import '../../core/CustomNavigator.dart';
import '../../exceptions/RequestException.dart';
import '../../services/UploadService.dart';


class UploadController with ChangeNotifier {

  String? selectedFilePath;
  String? selectedFileName;
  bool private = false;
  final Uploadservice uploadService;

  UploadController(this.uploadService);

  Future<void> initData() async {

  }

  bool hasSelectedFile() {
    return selectedFilePath != null && selectedFileName != null;
  }

  void setPrivate(bool? value) {
    private = value ?? false;
    notifyListeners();
  }


  Future<void> selectFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav', 'm4a', 'flac'],
      allowMultiple: false,
    );

    if (result != null) {
      selectedFilePath = result.files.single.path;
      selectedFileName = result.files.single.name;
      notifyListeners();
    } else {
      DialogBuilder.warning("You haven't selected any file", "To upload a new song to your library, please select a file.");
    }
  }

  Future<void> uploadSelectedFile() async {
    if (!hasSelectedFile()) {
      DialogBuilder.warning("You haven't selected any file", "To upload a new song to your library, please select a file.");
      return;
    }
    DialogBuilder.loading();
    try {
      final upload = await uploadService.uploadSong(selectedFilePath!, selectedFileName!, private);
      CustomNavigator.pushZoom(Uploadsuccessview(upload));
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (_) {
      DialogBuilder.appError();
    }

    notifyListeners();

  }
}