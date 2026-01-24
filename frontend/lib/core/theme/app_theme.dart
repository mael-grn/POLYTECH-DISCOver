import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

const  Color secondaryColor = Color(0xFF6A298F);
const Color primaryColor = Color(0xFF24578F);
const Color backgroundColor = Color(0xFF0E0E0E);
const Color backgroundVariantColor = Color(0xFF202020);
const Color foregroundColor = Color(0xFFF1F4F6);
const Color foregroundVariantColor = Color(0xFFC9DAEA);

const Color invalidColor = Color(0xFF7A2828);
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
