import 'package:flutter/material.dart';

class SlideFadeAnimationFromRightWidget extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final Curve curve;
  final Offset beginOffset;

  const SlideFadeAnimationFromRightWidget({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 400),
    this.curve = Curves.easeOut,
    this.beginOffset = const Offset(0.5, 0), // Décalage vertical initial
  });

  @override
  State<SlideFadeAnimationFromRightWidget> createState() => _SlideFadeAnimationFromRightWidgetState();
}

class _SlideFadeAnimationFromRightWidgetState extends State<SlideFadeAnimationFromRightWidget> {
  double _opacity = 0.0;
  Offset _offset = Offset.zero;

  @override
  void initState() {
    super.initState();
    _offset = widget.beginOffset;
    Future.delayed(Duration.zero, () {
      setState(() {
        _opacity = 1.0;
        _offset = Offset.zero;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedSlide(
      offset: _offset,
      duration: widget.duration,
      curve: widget.curve,
      child: AnimatedOpacity(
        opacity: _opacity,
        duration: widget.duration,
        curve: widget.curve,
        child: widget.child,
      ),
    );
  }
}