import 'package:discover/controllers/gestionPersonneExempleController.dart';
import 'package:discover/services/PersonneExempleService.dart';
import 'package:discover/views/GestionPersonneExempleView.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'core/theme/app_theme.dart';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void main() async {

  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent, // Couleur de fond de la barre d'état
    statusBarIconBrightness: Brightness.dark, // Pour des icônes noires sur fond clair
  ));

  final personneExempleService = PersonneExampleService();

  runApp(
    MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => GestionPersonnExempleController(personneExempleService)),
        ],
        child: MaterialApp(
          title: 'DISCOver',
          debugShowCheckedModeBanner: false,
          theme: appTheme,
          navigatorKey: navigatorKey,
          home: GestionPersonneExempleView(),
        )
    ),
  );
}


