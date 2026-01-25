import 'package:flutter/cupertino.dart';

class CustomPageRouteFromBottom<T> extends PageRouteBuilder<T> {
  CustomPageRouteFromBottom({required WidgetBuilder builder})
      : super(
    transitionDuration: const Duration(milliseconds: 1000),
    pageBuilder: (context, animation, secondaryAnimation) => builder(context),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final slide = Tween<Offset>(begin: const Offset(0.0, 3.0), end: Offset.zero)
          .animate(CurvedAnimation(parent: animation, curve: Curves.fastEaseInToSlowEaseOut));

      return SlideTransition(
          position: slide,
          child: child
      );
    },
  );
}

class CustomPageRouteFromRight<T> extends PageRouteBuilder<T> {
  CustomPageRouteFromRight({required WidgetBuilder builder})
      : super(
    transitionDuration: const Duration(milliseconds: 1000),
    pageBuilder: (context, animation, secondaryAnimation) => builder(context),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final slide = Tween<Offset>(begin: const Offset(3.0, 0.0), end: Offset.zero)
          .animate(CurvedAnimation(parent: animation, curve: Curves.fastEaseInToSlowEaseOut));

      return SlideTransition(
          position: slide,
          child: child
      );
    },
  );
}

class CustomZoomPageRoute<T> extends PageRouteBuilder<T> {
  final WidgetBuilder builder;

  CustomZoomPageRoute({required this.builder})
      : super(
    transitionDuration: const Duration(milliseconds: 600),
    pageBuilder: (context, animation, secondaryAnimation) => builder(context),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {

      final scale = Tween<double>(begin: 0.8, end: 1.0).animate(
        CurvedAnimation(
          parent: animation,
          curve: Curves.fastEaseInToSlowEaseOut,
        ),
      );

      final fade = Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(
          parent: animation,
          curve: const Interval(0.0, 0.5),
        ),
      );

      return FadeTransition(
        opacity: fade,
        child: ScaleTransition(
          scale: scale,
          child: child,
        ),
      );
    },
  );
}

