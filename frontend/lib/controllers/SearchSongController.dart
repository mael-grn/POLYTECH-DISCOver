import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/exceptions/RequestException.dart';
import 'package:flutter/cupertino.dart';
import '../models/Song.dart';
import '../services/SearchService.dart';

class SearchSongController with ChangeNotifier {

  SearchSongController();

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
      searchResults = await SearchService.searchSongs(query);
      hasSearched = true;
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

  void onSearchResultPressed(int songIndex) {
    DialogBuilder.warning("Not so fast!", "Not implemented yet...");
  }
}
