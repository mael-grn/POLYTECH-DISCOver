import 'package:discover/models/Song.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class SongView extends StatelessWidget {
  final Song song;
  final double? predictedPopularity;
  const SongView(this.song, this.predictedPopularity, {super.key});

  @override
  Widget build(BuildContext context) {
    return PageWidget(
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            LordiconWidget("doodle-music"),
            Text(
              song.name,
              style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 35),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 7),
            Text(
              song.getFormatedDuration(),
              style: const TextStyle(fontWeight: FontWeight.w300, fontSize: 17),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            ContainerWidget(
              Column(
                children: [
                  LordiconWidget("speaker", loop: true, size: 100),
                  const Text(
                    "Loudness",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    "${song.loudness} dB",
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            if (predictedPopularity != null) const SizedBox(height: 30),
            if (predictedPopularity != null) ContainerWidget(
              Column(
                children: [
                  LordiconWidget("trends", loop: true, size: 100,),
                  const Text(
                    "Predicted popularity",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    "${(predictedPopularity!*100).round()}%",
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),
            ContainerWidget(
              Column(
                children: [
                  LordiconWidget(song.isInDataset ? "server" : "cloud-user", loop: true, size: 100, key:Key(song.isInDataset.toString()) ,),
                  Text(
                    song.isInDataset ? "This song comes from our database." : "This song has been uploaded by another user.",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            if (song.isInDataset) ...[
              _buildStatBar("Danceability", song.danceability),
              _buildStatBar("Energy", song.energy),
              _buildStatBar("Acousticness", song.acousticness),
              _buildStatBar("Instrumentalness", song.instrumentalness),
              _buildStatBar("Liveness", song.liveness),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatBar(String label, double value) {
    return Padding(
      padding: const EdgeInsets.only(top: 15),
      child: ContainerWidget(
        Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  label,
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                ),
                Text(
                  "${(value * 100).toStringAsFixed(1)}%",
                  style: const TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                ),
              ],
            ),
            const SizedBox(height: 10),
            ClipRRect(
              borderRadius: BorderRadius.circular(5),
              child: LinearProgressIndicator(
                value: value,
                backgroundColor: backgroundColor,
                valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
              ),
            ),
          ],
        ),
      ),
    );
  }
}