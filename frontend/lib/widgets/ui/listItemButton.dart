import 'package:discover/widgets/animations/scale_pop_animation_widget.dart';
import 'package:discover/widgets/ui/lordicon_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/theme/app_theme.dart';

class ListItemButton extends StatelessWidget {
  final String title;
  final VoidCallback onPressed;
  final IconData? icon;
  const ListItemButton({
    required this.title,
    required this.onPressed,
    this.icon,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ScalePopAnimationWidget(
      child: InkWell(
        onTap: () {
          HapticFeedback.mediumImpact();
          onPressed();
        },
        child: Container(
          padding: const EdgeInsets.all(15),
          decoration: BoxDecoration(
            color: backgroundColor,
            borderRadius: BorderRadius.circular(20),
          ),
          width: double.infinity,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              IconButton(
                icon: Icon(icon ?? Icons.settings),
                iconSize: 30,
                color: foregroundColor,
                onPressed: onPressed,
              ),
              Text(
                title,
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  fontSize: 20,
                ),
              ),
              IconButton(
                icon: Icon(Icons.arrow_forward_ios_rounded),
                iconSize: 30,
                color: foregroundColor,
                onPressed: onPressed,
              )
            ],
          ),
        ),
      ),
    );
  }
}
