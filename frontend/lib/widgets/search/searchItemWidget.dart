import 'package:discover/widgets/animations/scale_pop_animation_widget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../../core/theme/app_theme.dart';

class SearchItemWidget extends StatelessWidget {
  final String title;
  final String subtitle;
  final String? coverUrl;
  final VoidCallback onPressed;

  const SearchItemWidget({required this.title, required this.subtitle, this.coverUrl, required this.onPressed, super.key});

  @override
  Widget build(BuildContext context) {


    return ScalePopAnimationWidget(
      child: InkWell(
        onTap: onPressed,
        child: Container(
          width: double.infinity,
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: backgroundVariantColor,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Row(
              children: [
                coverUrl == null ?
                LordiconWidget("doodle-music", size: 50,) :
                Image.network(coverUrl!, width: 50, height: 50,),
                SizedBox(width: 15,),
                Column(
                  children: [
                    Text(
                      title,
                      style: TextStyle(fontWeight: FontWeight.w600, fontSize: 20),
                    ),
                    SizedBox(height: 5,),
                    Text(
                      subtitle,
                      style: TextStyle(fontWeight: FontWeight.w300, fontSize: 16),
                    ),
                  ],
                )
              ]
          ),
        ),
      )
    );
  }
}
