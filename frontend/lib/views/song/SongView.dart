import 'package:discover/controllers/song/SongController.dart';
import 'package:discover/models/Song.dart';
import 'package:discover/widgets/ui/ButtonWidget.dart';
import 'package:discover/widgets/ui/ContainerWidget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import 'package:provider/provider.dart';

class SongView extends StatefulWidget {
  final Song song;
  final double? predictedPopularity;
  SongView(this.song, this.predictedPopularity, {super.key});

  @override
  State<SongView> createState() => _SongView();
}


class _SongView extends State<SongView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<SongController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final controller = context.watch<SongController>();

    return PageWidget(
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            LordiconWidget("doodle-music"),
            Text(
              widget.song.name,
              style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 35),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 7),
            Text(
              widget.song.getFormatedDuration(),
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
                    "${widget.song.loudness} dB",
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            if (widget.predictedPopularity != null) const SizedBox(height: 30),
            if (widget.predictedPopularity != null) ContainerWidget(
              Column(
                children: [
                  LordiconWidget("trends", loop: true, size: 100,),
                  const Text(
                    "Predicted popularity",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    "${(widget.predictedPopularity!*100).toStringAsFixed(2)}%",
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
                  LordiconWidget("cloud-plus", loop: true, size: 100,),
                  Text(
                     controller.analyzePreview == null ? "Preview another analyze" : "Analyze preview",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  if (controller.analyzePreview == null) Text(
                    "You can generate a new analyze of this song. It will not be saved.",
                    style: const TextStyle(fontWeight: FontWeight.w400, fontSize: 18),
                    textAlign: TextAlign.center,
                  )
                  else Text(
                    "${(controller.analyzePreview!.predictedPopularity)}%",
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10,),
                  ButtonWidget(
                      message: "Generate preview",
                      icon: Icons.loop,
                      onPressed: () => controller.onAnalyzePreviewPressed(widget.song.id)
                  )
                ],
              ),
            ),
            if (widget.song.tempo != null) const SizedBox(height: 30),
            if (widget.song.tempo != null) ContainerWidget(
              Column(
                children: [
                  const Text(
                    "Tempo",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    "${widget.song.tempo} BMP",
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            if (widget.song.isInDataset) ...[
              _buildStatBar("Danceability", widget.song.danceability),
              _buildStatBar("Energy", widget.song.energy),
              _buildStatBar("Acousticness", widget.song.acousticness),
              _buildStatBar("Instrumentalness", widget.song.instrumentalness),
              _buildStatBar("Liveness", widget.song.liveness),
            ],
            const SizedBox(height: 30),
            ContainerWidget(
              Column(
                children: [
                  LordiconWidget(widget.song.isInDataset ? "server" : "cloud-user", loop: true, size: 100, key:Key(widget.song.isInDataset.toString()) ,),
                  Text(
                    widget.song.isInDataset ? "This song comes from our database." : "This song has been uploaded.",
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
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