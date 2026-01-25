import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'PageRoute.dart';
import '../views/GlobalLayout.dart';
import 'global.dart';

class CustomNavigator {

  // 1. On crée un "raccourci" qui va chercher l'état actuel du navigateur
  // à chaque fois qu'on l'appelle.
  static NavigatorState? get _navigator => navigatorKey.currentState;

  // 2. Plus besoin de passer de contexte en paramètre
  static void pushFromBottom(Widget newPage) {
    _navigator?.push(
      CustomPageRouteFromBottom(
        builder: (_) => newPage,
      ),
    );
  }

  static void resetToHome() {
    // Cette fonction nettoie tout l'historique et relance GlobalLayout
    _navigator?.pushAndRemoveUntil(
      MaterialPageRoute(
        builder: (context) => const GlobalLayout(),
      ),
          (Route route) => false,
    );
  }

  static void pushFromRight(Widget newPage) {
    _navigator?.push(
      CustomPageRouteFromRight(
        builder: (_) => newPage,
      ),
    );
  }

  static void pushZoom(Widget newPage) {
    _navigator?.push(
      CustomZoomPageRoute(
        builder: (_) => newPage,
      ),
    );
  }

  static void back() {
    if (_navigator?.canPop() == true) {
      _navigator?.pop();
    }
  }

  static void pushReplacementFromBottom(Widget newPage) {
    _navigator?.pushReplacement(
      CustomPageRouteFromBottom(
        builder: (_) => newPage,
      ),
    );
  }

  static void pushReplacementFromRight(Widget newPage) {
    _navigator?.pushReplacement(
      CustomPageRouteFromRight(
        builder: (_) => newPage,
      ),
    );
  }
}