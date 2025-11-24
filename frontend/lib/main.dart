import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/controllers/HomeController.dart';
import 'package:discover/controllers/UploadController.dart';
import 'package:discover/controllers/gestionPersonneExempleController.dart';
import 'package:discover/services/PersonneExempleService.dart';
import 'package:discover/views/GlobalLayout.dart';
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
          ChangeNotifierProvider(create: (_) => HomeController()),
          ChangeNotifierProvider(create: (_) => ExploreController()),
          ChangeNotifierProvider(create: (_) => UploadController()),
          ChangeNotifierProvider(create: (_) => AccountController()),
        ],
        child: MaterialApp(
          title: 'DISCOver',
          debugShowCheckedModeBanner: false,
          theme: appTheme,
          navigatorKey: navigatorKey,
          home: GlobalLayout(),
        )
    ),
  );
}


