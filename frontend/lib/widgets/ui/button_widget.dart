import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:discover/core/theme/app_theme.dart';

import '../../core/theme/app_theme.dart' as app_theme;

enum ButtonWidgetSize {
  small(10.0),
  medium(20.0),
  large(30.0);

  final double value;

  const ButtonWidgetSize(this.value);
}

class ButtonWidget extends StatelessWidget {
  final String message;
  final IconData icon;
  final Color backgroundColor;
  final Color foregroundColor;
  final VoidCallback onPressed;
  final EdgeInsetsGeometry padding;
  final bool iconOnRight;
  final String? tag;
  final bool disabled;

  const ButtonWidget({
    super.key,
    required this.message,
    required this.icon,
    this.foregroundColor = app_theme.backgroundColor,
    this.backgroundColor = primaryColor,
    required this.onPressed,
    this.padding = const EdgeInsets.symmetric(vertical: 15, horizontal: 25),
    this.iconOnRight = false,
    this.tag,
    this.disabled = false,
  });

  @override
  Widget build(BuildContext context) {
    final children = <Widget>[
      if (!iconOnRight) Icon(icon, size: 22),
      if (!iconOnRight) SizedBox(width: 10),
      Text(message),
      if (iconOnRight) SizedBox(width: 10),
      if (iconOnRight) Icon(icon, size: 22),
    ];

    return Hero(
        tag: tag ?? "hero-$message",
        child: ElevatedButton(

          style: ElevatedButton.styleFrom(
            backgroundColor: disabled ? backgroundVariantColor : backgroundColor,
            foregroundColor: foregroundColor,
            elevation: 4,
            shadowColor: primaryColor.withAlpha((0.3 * 255).round()),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            padding: padding,
            textStyle: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 16,
              fontFamily: 'Poppins',
            ),
          ),
          onPressed: () {
            if (!disabled) {
              HapticFeedback.mediumImpact();
              onPressed();
            }
          },
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Flex(
              direction: Axis.horizontal,
              mainAxisSize: MainAxisSize.min,
              children: children,
            ),
          )
        )
    );
  }
}