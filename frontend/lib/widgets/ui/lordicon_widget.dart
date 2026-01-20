import 'package:flutter/material.dart'; // Préférable à cupertino pour la compatibilité générale
import 'package:lordicon/lordicon.dart';

class LordiconWidget extends StatefulWidget {
  final String iconName;
  final bool loop;
  final VoidCallback? onTap;
  final Color? color;
  final double size;

  const LordiconWidget(this.iconName, {
    super.key,
    this.onTap,
    this.loop = false,
    this.color,
    this.size = 200
  });

  @override
  State<LordiconWidget> createState() => _LordiconWidgetState();
}

class _LordiconWidgetState extends State<LordiconWidget> {
  late IconController _controller;

  @override
  void initState() {
    super.initState();
    _controller = IconController.assets("icons/${widget.iconName}.json");

    _controller.addStatusListener((status) {
      if (status == ControllerStatus.ready) {
        _controller.playFromBeginning();
      }
      if (status == ControllerStatus.completed) {
        if (widget.loop) {
          _controller.playFromBeginning();
        } else {
          _controller.goToFirstFrame();
        }
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        _controller.playFromBeginning();
        widget.onTap?.call();
      },
      child: IconViewer(
        controller: _controller,
        width: widget.size,
        height: widget.size,
        colorize: widget.color,
      ),
    );
  }
}