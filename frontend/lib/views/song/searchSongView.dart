import 'package:discover/controllers/SearchSongController.dart';
import 'package:discover/widgets/search/songListItemWidget.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/Song.dart';

class SearchSongView extends StatefulWidget {
  SearchSongView({super.key});

  @override
  State<SearchSongView> createState() => _SearchSongView();
}

class _SearchSongView extends State<SearchSongView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<SearchSongController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<SearchSongController>();

    return PageWidget(
        body: SingleChildScrollView(
          child: Column(
            children: [
              TextInputWidget(
                controller: controller.searchQueryController,
                hint: "Artists, songs, ...",
                icon: Icons.search,
                big: true,
                onIconClick: () => controller.searchSongs(),
              ),
              const SizedBox(height: 40),

              controller.searchResults.isEmpty
                  ? controller.hasSearched
                  ? Center(
                child: ContainerWidget(
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Image.asset(
                        "images/team/nahel-search.png",
                        height: 200,
                      ),
                      const SizedBox(height: 15),
                      const Text(
                        "No song found",
                        style: TextStyle(fontSize: 18),
                      ),
                    ],
                  ),
                ),
              )
                  : Center(
                child: ContainerWidget(
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      LordiconWidget("search"),
                      const SizedBox(height: 15),
                      const Text(
                        "Start by searching for a song",
                        style: TextStyle(fontSize: 18),
                      ),
                    ],
                  ),
                ),
              )
                  : ListView.builder(
                itemCount: controller.searchResults.length,
                itemBuilder: (context, index) {
                  final Song song = controller.searchResults[index];
                  return SongListItemWidget(
                    title: song.name,
                    onPressed: () => controller.onSearchResultPressed(index),
                  );
                },
              ),
            ],
          ),
        )
    );
  }
}
