import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

const  Color secondaryColor = Color(0xFF695C7B);
const Color primaryColor = Color(0xFF977086);
const Color backgroundColor = Color(0xFF021334);
const Color backgroundVariantColor = Color(0xFF012A61);
const Color foregroundColor = Color(0xFFE9F3F5);
const Color foregroundVariantColor = Color(0xFFAFC7DD);

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
  textTheme: TextTheme(
    bodySmall: GoogleFonts.poppins(
      color: foregroundColor
    ),
    bodyMedium: GoogleFonts.poppins(
        color: foregroundColor
    ),
    bodyLarge: GoogleFonts.poppins(
        color: foregroundColor
    ),
    headlineSmall: GoogleFonts.poppins(
        color: foregroundColor
    ),
    headlineMedium: GoogleFonts.poppins(
        color: foregroundColor
    ),
    headlineLarge: GoogleFonts.poppins(
        color: foregroundColor
    )
  ),
  textButtonTheme: TextButtonThemeData(
    style: TextButton.styleFrom(
      foregroundColor: foregroundColor,
      textStyle: GoogleFonts.poppins(
        fontWeight: FontWeight.w800,
        color: foregroundColor,
      ),
      backgroundColor: Colors.transparent,
    ),
  ),
  scaffoldBackgroundColor: backgroundColor,
);
