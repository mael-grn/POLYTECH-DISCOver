import 'package:flutter/cupertino.dart';
import '../main.dart';
import 'PageRoute.dart';

class CustomNavigator {
  static final context = navigatorKey.currentContext;
  static const heroTag = "hero";
  
  static void pushFromBottom(Widget newPage, {BuildContext? otherContext}) {
    if (context == null) {
      return;
    }
    Navigator.of(otherContext ?? context!).push(
      CustomPageRouteFromBottom(
        builder: (_) => newPage,
      ),
    );
  }

  static void pushFromRight(Widget newPage, {BuildContext? otherContext}) {
    if (context == null) {
      return;
    }
    Navigator.of(otherContext ?? context!).push(
      CustomPageRouteFromRight(
        builder: (_) => newPage,
      ),
    );
  }

  static void back() {
    if (context == null) {
      return;
    }
    Navigator.of(context!).pop();
  }

  static void pushReplacementFromBottom(Widget newPage) {
    if (context == null) {
      return;
    }
    Navigator.of(context!).pushReplacement(
      CustomPageRouteFromBottom(
        builder: (_) => newPage,
      ),
    );
  }

  static void pushReplacementFromRight(Widget newPage) {
    if (context == null) {
      return;
    }
    Navigator.of(context!).pushReplacement(
      CustomPageRouteFromRight(
        builder: (_) => newPage,
      ),
    );
  }
}