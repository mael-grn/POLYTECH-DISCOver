import 'package:discover/controllers/song/SearchSongController.dart';
import 'package:discover/widgets/search/SongListItemWidget.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
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
              LordiconWidget("search"),
              SizedBox(height: 15,),
              Text(
                "Search for any song",
                style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 20,),
              ContainerWidget(
                Column(
                  children: [
                    TextInputWidget(
                      controller: controller.searchQueryController,
                      hint: "Artists, songs, ...",
                      icon: Icons.search,
                      big: true,
                      onIconClick: () => controller.searchSongs(),
                    ),
                    SizedBox(height: 40),

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
                            const SizedBox(height: 15),
                            const Text(
                              "Start by searching for a song",
                              style: TextStyle(fontSize: 18),
                            ),
                          ],
                        ),
                      ),
                    )
                        : ListView.separated(
                      separatorBuilder: (context, index) =>
                          SizedBox(height: 10),
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
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
                )
              ),

            ],
          ),
        )
    );
  }
}
