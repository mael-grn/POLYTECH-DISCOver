import 'package:discover/widgets/animations/ScalePopAnimationWidget.dart';
import 'package:flutter/cupertino.dart';

import '../../core/theme/app_theme.dart';

class ContainerWidget extends StatelessWidget {
  final Widget child;

  const ContainerWidget(this.child, {super.key});

  @override
  Widget build(BuildContext context) {


    return ScalePopAnimationWidget(
        child: Container(
          width: 800,
          padding: EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: backgroundVariantColor,
            borderRadius: BorderRadius.circular(20),
          ),
          child: child,
        ),
    );
  }
}
