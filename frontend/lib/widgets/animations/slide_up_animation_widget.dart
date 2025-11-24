import 'package:flutter/material.dart';

class SlideUpAnimationWidget extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final Curve curve;
  final Offset beginOffset;

  const SlideUpAnimationWidget({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 700),
    this.curve = Curves.fastEaseInToSlowEaseOut,
    this.beginOffset = const Offset(0, 1), // Décalage vertical initial
  });

  @override
  State<SlideUpAnimationWidget> createState() => _SlideUpAnimationWidgetState();
}

class _SlideUpAnimationWidgetState extends State<SlideUpAnimationWidget> {
  Offset _offset = Offset.zero;

  @override
  void initState() {
    super.initState();
    _offset = widget.beginOffset;
    Future.delayed(Duration.zero, () {
      setState(() {
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
      child: widget.child
    );
  }
}