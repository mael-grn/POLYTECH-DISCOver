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

