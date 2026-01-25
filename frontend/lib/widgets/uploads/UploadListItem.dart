import 'package:discover/models/Upload.dart';
import 'package:discover/utils/StringUtils.dart';
import 'package:discover/widgets/animations/ScalePopAnimationWidget.dart';
import 'package:discover/widgets/ui/LordiconWidget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/theme/app_theme.dart';

class UploadListItemWidget extends StatelessWidget {
  final Upload upload;
  final VoidCallback onItemPressed;

  const UploadListItemWidget({
    required this.upload,
    required this.onItemPressed,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ScalePopAnimationWidget(
      child: InkWell(
        onTap: () {
          HapticFeedback.mediumImpact();
          onItemPressed();
        },
        child:Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: backgroundColor,
            borderRadius: BorderRadius.circular(20),
          ),
          width: double.infinity,
          child: Row(
            children: [
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: upload.private ? secondaryColor : primaryColor,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Center(
                  child: Icon(
                    upload.private ? Icons.lock : Icons.public,
                    color: Colors.white,
                    size: 30,
                  ),
                ),
              ),
              SizedBox(width: 10,),
              Expanded(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      upload.songName,
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                      style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(height: 5),
                    Text(
                      upload.getFormatedDuration(),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                      style: TextStyle(
                        fontWeight: FontWeight.w300,
                        fontSize: 16,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(width: 10,),

              Text(
                "${upload.predictedPopularity}%",
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
                style: TextStyle(
                  fontWeight: FontWeight.w900,
                  fontSize: 30,
                ),
              ),
            ],
          ),
        ),
      )
    );
  }
}
