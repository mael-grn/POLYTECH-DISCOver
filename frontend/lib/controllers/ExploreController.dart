import 'package:flutter/cupertino.dart';
import '../models/Song.dart';
import '../services/SearchService.dart';

class ExploreController with ChangeNotifier {

  ExploreController();

  final searchQueryController = TextEditingController();
  List<Song> searchResults = [];
  bool isLoading = false;

  Future<void> initData() async {
    // Rien pour l'instant
  }

  Future<void> searchSongs() async {
    final query = searchQueryController.text.trim();
    if (query.isEmpty) return;

    isLoading = true;
    notifyListeners();

    try {
      searchResults = await SearchService.searchSongs(query);
    } catch (e) {
      searchResults = [];
      // Ici tu pourrais afficher un dialog d'erreur
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
