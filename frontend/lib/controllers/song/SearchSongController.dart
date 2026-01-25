import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/exceptions/RequestException.dart';
import 'package:flutter/cupertino.dart';
import '../../core/CustomNavigator.dart';
import '../../models/Song.dart';
import '../../services/SongService.dart';
import '../../views/song/SongView.dart';

class SearchSongController with ChangeNotifier {

  SearchSongController(this.songService);

  final SongService songService;

  final searchQueryController = TextEditingController();
  List<Song> searchResults = [];
  bool hasSearched = false;

  Future<void> initData() async {
    // Rien pour l'instant
  }

  Future<void> searchSongs() async {
    final query = searchQueryController.text.trim();
    if (query.isEmpty) {
      DialogBuilder.warning("Not so fast!", "You must enter a query in the appropriate field to initiate a search.");
      return;
    }
    DialogBuilder.loading();
    try {
      searchResults = await songService.searchSongs(query);
      hasSearched = true;
      DialogBuilder.closeCurrentDialog();
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
      searchResults = [];
      hasSearched = false;
    } catch (_) {
      DialogBuilder.appError();
      searchResults = [];
      hasSearched = false;
    } finally {
      notifyListeners();
    }
  }

  void onSearchResultPressed(int songIndex) async {
    DialogBuilder.loading();
    try {
      Song song = await songService.getSongById(searchResults[songIndex].id);
      double? analyze = await songService.getAnalyzeBySongId(song.id);
      DialogBuilder.closeCurrentDialog();
      CustomNavigator.pushFromBottom(SongView(song, analyze));
    } on NetworkException catch (e) {
      DialogBuilder.networkError(e.networkError);
    } catch (e) {
      DialogBuilder.appError();
    }
  }
}
