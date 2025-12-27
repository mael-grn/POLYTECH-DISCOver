import 'package:flutter/cupertino.dart';
import 'package:lordicon/lordicon.dart';

import '../../core/theme/app_theme.dart';

class LordiconWidget extends StatelessWidget {
  final String iconName;
  final bool loop;
  final Function? onTap;
  final Color? color;
  final double size;
  const LordiconWidget(this.iconName, {super.key, this.onTap, this.loop = false, this.color, this.size = 200});

  @override
  Widget build(BuildContext context) {
    var controller = IconController.assets("icons/$iconName.json");

    controller.addStatusListener((status) {
      if (status == ControllerStatus.ready) {
        controller.playFromBeginning();
      }
      if (status == ControllerStatus.completed) {
        if (loop) {
          controller.playFromBeginning();
        } else {
          controller.goToFirstFrame();
        }
      }
    });

    return GestureDetector(
      onTap: () {
        if (onTap != null) {
          controller.playFromBeginning();
          onTap?.call();
        }
      },
      child: IconViewer(
        controller: controller,
        width: size,
        height: size,
        colorize: color,
      ),
    );
  }
}
