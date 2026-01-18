import 'package:flutter/material.dart';

class ScalePopAnimationWidget extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final Curve curve;

  const ScalePopAnimationWidget({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 700),
    this.curve = Curves.elasticOut,
  });

  @override
  State<ScalePopAnimationWidget> createState() => _ScalePopAnimationWidgetState();
}

class _ScalePopAnimationWidgetState extends State<ScalePopAnimationWidget> {
  double _scale = 0.0;

  @override
  void initState() {
    super.initState();
    // Démarre l’animation au prochain frame
    Future.delayed(Duration.zero, () {
      setState(() {
        _scale = 1.0;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedScale(
      scale: _scale,
      duration: widget.duration,
      curve: widget.curve,
      child: widget.child,
    );
  }
}