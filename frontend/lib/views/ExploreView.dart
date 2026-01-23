import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/Song.dart';
import '../widgets/search/songListItemWidget.dart';
import '../widgets/ui/button_widget.dart';
import '../widgets/ui/lordicon_widget.dart';

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
          ContainerWidget(
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                LordiconWidget("search"),
                SizedBox(height: 10),
                Text(
                  "Want to look for an existing song in our dataset?",
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),
                ButtonWidget(
                  message: "Start searching",
                  icon: Icons.search,
                  onPressed: controller.onSearchSongClicked,
                ),
              ],
            ),
          ),
          SizedBox(height: 20),
          ContainerWidget(
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                LordiconWidget("clock"),
                SizedBox(height: 10),
                Text(
                  "History",
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),
                controller.history.isEmpty
                    ? Text(
                        "No history yet",
                        style: TextStyle(
                          fontWeight: FontWeight.w300,
                          fontSize: 18,
                        ),
                        textAlign: TextAlign.center,
                      )
                    : ListView.separated(
                        shrinkWrap: true,
                        separatorBuilder: (context, index) =>
                            SizedBox(height: 10),
                        physics: NeverScrollableScrollPhysics(),
                        itemCount: controller.history.length,
                        itemBuilder: (context, index) {
                          final Song song = controller.history[index];
                          return SongListItemWidget(
                            title: song.name,
                            onPressed: () =>
                                controller.onSongItemPressed(index),
                          );
                        },
                      ),
              ],
            ),
          ),
          SizedBox(height: 120),
        ],
      ),
    );
  }
}
