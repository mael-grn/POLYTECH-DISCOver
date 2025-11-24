import 'package:flutter/material.dart';

const  Color secondaryColor = Color(0xFF87DFBA);
const Color primaryColor = Color(0xFF58AC88);
const Color backgroundColor = Color(0xFFFFFFFF);
const Color backgroundVariantColor = Color(0xFFC6D1D0);
const Color foregroundColor = Color(0xFF000000);
const Color foregroundVariantColor = Color(0xFF282E28);

const Color invalidColor = Colors.redAccent;
const Color validColor = Color(0xFF58AC88);

final MaterialColor customColor = MaterialColor(
  0xFFAABBFF,
  <int, Color>{
    50: foregroundColor,
    100: primaryColor,
    200: primaryColor,
    300: primaryColor,
    400: primaryColor,
    500: primaryColor,
    600: primaryColor,
    700: primaryColor,
    800: primaryColor,
    900: backgroundColor,
  },
);

final ThemeData appTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.light,
  primarySwatch: customColor,
  visualDensity: VisualDensity.adaptivePlatformDensity,
  fontFamily: 'Poppins',
  textTheme: TextTheme(
    bodySmall: TextStyle(
      fontFamily: 'Poppins',
    ),
    bodyMedium: TextStyle(
      fontFamily: 'Poppins',
    ),
    bodyLarge: TextStyle(
      fontFamily: 'Poppins',
    ),
    headlineSmall: TextStyle(
      fontFamily: 'Poppins',
    ),
    headlineMedium: TextStyle(
      fontFamily: 'Poppins',
    ),
    headlineLarge: TextStyle(
      fontFamily: 'Poppins',
    )
  ),
  textButtonTheme: TextButtonThemeData(
    style: TextButton.styleFrom(
      foregroundColor: foregroundColor,
      textStyle: TextStyle(
        fontWeight: FontWeight.w800,
        fontFamily: 'Poppins',
        color: foregroundColor,
      ),
      backgroundColor: Colors.transparent,
    ),
  ),
  scaffoldBackgroundColor: backgroundColor,
);