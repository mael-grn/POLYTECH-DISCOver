import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/widgets/search/searchItemWidget.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/Song.dart';

class ExploreView extends StatefulWidget {
  ExploreView({super.key});

  @override
  State<ExploreView> createState() => _ExploreView();
}

class _ExploreView extends State<ExploreView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ExploreController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<ExploreController>();

    return SingleChildScrollView(
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
                    return SearchItemWidget(
                      title: song.name,
                      subtitle: "${song.artist} • ${song.album}",
                      onPressed: () => controller.onSearchResultPressed(index),
                    );
                  },
                ),
        ],
      ),
    );
  }
}
