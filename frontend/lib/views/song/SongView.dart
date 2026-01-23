import 'package:discover/models/Song.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:discover/widgets/ui/text_info_widget.dart';
import 'package:flutter/cupertino.dart';

class SongView extends StatelessWidget {
  final Song song;

  const SongView(this.song, {super.key});

  @override
  Widget build(BuildContext context) {
    return PageWidget(
      body: SingleChildScrollView(
          child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                LordiconWidget("speaker"),
                Text(
                  song.name,
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 35),
                  textAlign: TextAlign.center,
                ),
                ContainerWidget(
                  Column(
                    children: [
                      TextInfoWidget("Duration:", "${song.duration}s"),
                      TextInfoWidget("Genre:", "${song.genre}s"),
                    ],
                  ),
                )
              ]
          )
      ),
    );
  }
}
