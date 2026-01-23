import 'package:discover/models/Song.dart';
import 'package:discover/widgets/ui/Container_widget.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:discover/widgets/ui/text_info_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../../core/theme/app_theme.dart';

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
                LordiconWidget("doodle-music"),
                Text(
                  song.name,
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 35),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 7,),
                Text(
                  song.getFormatedDuration(),
                  style: TextStyle(fontWeight: FontWeight.w300, fontSize: 17),
                  textAlign: TextAlign.center,
                ),

                SizedBox(height: 30,),
                ContainerWidget(
                    Column(
                      children: [
                        LordiconWidget("speaker", loop: true, size: 100),
                        Text(
                          "Loudness",
                          style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                          textAlign: TextAlign.center,
                        ),
                        Text(
                          "${song.loudness} dB",
                          style: TextStyle(fontWeight: FontWeight.w900, fontSize: 35),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    )
                ),
                SizedBox(height: 15,),

                ContainerWidget(
                  Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Danceability",
                            style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                          ),
                          Text(
                            "${(song.danceability * 100).toStringAsFixed(1)}%",
                            style: TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                          ),
                        ],
                      ),
                      SizedBox(height: 10,),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(5),
                        child: LinearProgressIndicator(
                          value: song.danceability,
                          backgroundColor: backgroundColor,
                          valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
                        ),
                      ),
                    ],
                  )
                ),

                SizedBox(height: 15,),
                ContainerWidget(
                    Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Energy",
                              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                            ),
                            Text(
                              "${(song.energy * 100).toStringAsFixed(1)}%",
                              style: TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                            ),
                          ],
                        ),
                        SizedBox(height: 10,),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(5),
                          child: LinearProgressIndicator(
                            value: song.energy,
                            backgroundColor: backgroundColor,
                            valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
                          ),
                        ),
                      ],
                    )
                ),

                SizedBox(height: 15,),
                ContainerWidget(
                    Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Acousticness",
                              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                            ),
                            Text(
                              "${(song.acousticness * 100).toStringAsFixed(1)}%",
                              style: TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                            ),
                          ],
                        ),
                        SizedBox(height: 10,),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(5),
                          child: LinearProgressIndicator(
                            value: song.acousticness,
                            backgroundColor: backgroundColor,
                            valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
                          ),
                        ),
                      ],
                    )
                ),

                SizedBox(height: 15,),
                ContainerWidget(
                    Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Instrumentalness",
                              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                            ),
                            Text(
                              "${(song.instrumentalness * 100).toStringAsFixed(1)}%",
                              style: TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                            ),
                          ],
                        ),
                        SizedBox(height: 10,),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(5),
                          child: LinearProgressIndicator(
                            value: song.instrumentalness,
                            backgroundColor: backgroundColor,
                            valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
                          ),
                        ),
                      ],
                    )
                ),

                SizedBox(height: 15,),
                ContainerWidget(
                    Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Liveness",
                              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                            ),
                            Text(
                              "${(song.liveness * 100).toStringAsFixed(1)}%",
                              style: TextStyle(fontWeight: FontWeight.w300, fontSize: 20),
                            ),
                          ],
                        ),
                        SizedBox(height: 10,),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(5),
                          child: LinearProgressIndicator(
                            value: song.liveness,
                            backgroundColor: backgroundColor,
                            valueColor: AlwaysStoppedAnimation<Color>(secondaryColor),
                          ),
                        ),
                      ],
                    )
                ),

                SizedBox(height: 15,),
                ContainerWidget(
                  Column(
                    children: [
                      LordiconWidget("file", size: 100),
                      SizedBox(height: 10),
                      Text(
                        "Raw data",
                        style: TextStyle(fontWeight: FontWeight.w600, fontSize: 25),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 15,),
                      TextInfoWidget("ID:", "${song.id}"),
                      TextInfoWidget("Name:", song.name),
                      TextInfoWidget("Duration:", "${song.duration}ms"),
                      TextInfoWidget("Danceability:", "${(song.danceability * 100).toStringAsFixed(1)}%"),
                      TextInfoWidget("Energy:", "${(song.energy * 100).toStringAsFixed(1)}%"),
                      TextInfoWidget("Acousticness:", "${(song.acousticness * 100).toStringAsFixed(1)}%"),
                      TextInfoWidget("Instrumentalness:", "${(song.instrumentalness * 100).toStringAsFixed(1)}%"),
                      TextInfoWidget("Liveness:", "${(song.liveness * 100).toStringAsFixed(1)}%"),
                      TextInfoWidget("Key:", "${song.key}"),
                      TextInfoWidget("Loudness:", "${song.loudness} dB"),
                      TextInfoWidget("In Dataset:", song.isInDataset ? "Yes" : "No"),
                    ],
                  ),
                )
              ]
          )
      ),
    );
  }
}
