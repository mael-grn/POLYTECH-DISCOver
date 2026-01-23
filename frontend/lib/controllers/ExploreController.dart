
import 'package:discover/core/CustomNavigator.dart';
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/models/Song.dart';
import 'package:discover/services/SongService.dart';
import 'package:discover/views/song/SongView.dart';
import 'package:discover/views/song/searchSongView.dart';
import 'package:discover/views/upload/UploadNewSongView.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

import '../exceptions/RequestException.dart';


class ExploreController with ChangeNotifier {

  ExploreController(this.songService);
  final SongService songService;

  List<Song> trends = [];

  Future<void> initData() async {
    try {
      trends = await songService.getSongs();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
    notifyListeners();
  }

  void onSearchSongClicked() {
    CustomNavigator.pushFromRight(SearchSongView());
  }

  void onUploadClicked() {
    CustomNavigator.pushFromRight(UploadNewSongView());
  }

  void onSongItemPressed(int index) async {
    DialogBuilder.loading();
    try {
      Song song = await songService.getSongById(trends[index].id);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.pushFromBottom(SongView(song));
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }
}