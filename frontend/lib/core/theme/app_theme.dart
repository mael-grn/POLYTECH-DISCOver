import 'package:flutter/material.dart';

const  Color secondaryColor = Color(0xFF695C7B);
const Color primaryColor = Color(0xFF977086);
const Color backgroundColor = Color(0xFF021334);
const Color backgroundVariantColor = Color(0xFF012A61);
const Color foregroundColor = Color(0xFFA5C5CC);
const Color foregroundVariantColor = Color(0xFF6CA5DB);

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
      color: foregroundColor
    ),
    bodyMedium: TextStyle(
      fontFamily: 'Poppins',
        color: foregroundColor
    ),
    bodyLarge: TextStyle(
      fontFamily: 'Poppins',
        color: foregroundColor
    ),
    headlineSmall: TextStyle(
      fontFamily: 'Poppins',
        color: foregroundColor
    ),
    headlineMedium: TextStyle(
      fontFamily: 'Poppins',
        color: foregroundColor
    ),
    headlineLarge: TextStyle(
      fontFamily: 'Poppins',
        color: foregroundColor
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