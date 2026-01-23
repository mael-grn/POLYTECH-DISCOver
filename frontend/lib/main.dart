import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/controllers/LoginController.dart';
import 'package:discover/controllers/SearchSongController.dart';
import 'package:discover/controllers/HomeController.dart';
import 'package:discover/controllers/registerController.dart';
import 'package:discover/controllers/upload/UploadController.dart';
import 'package:discover/controllers/gestionPersonneExempleController.dart';
import 'package:discover/controllers/upload/UploadSuccessController.dart';
import 'package:discover/services/AuthService.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/PersonneExempleService.dart';
import 'package:discover/services/SongService.dart';
import 'package:discover/services/UploadService.dart';
import 'package:discover/services/UserService.dart';
import 'package:discover/views/GlobalLayout.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'controllers/ServerStatusController.dart';
import 'core/global.dart';
import 'core/theme/app_theme.dart';

void main() async {

  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent, // Couleur de fond de la barre d'état
    statusBarIconBrightness: Brightness.dark, // Pour des icônes noires sur fond clair
  ));

  final personneExempleService = PersonneExampleService();
  final uploadService = Uploadservice();
  final songService = SongService();
  final healthService = Healthservice();
  final userService = UserService();
  final authService = AuthService();


  runApp(
    MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => GestionPersonnExempleController(personneExempleService)),
          ChangeNotifierProvider(create: (_) => HomeController(uploadService, songService)),
          ChangeNotifierProvider(create: (_) => SearchSongController()),
          ChangeNotifierProvider(create: (_) => UploadController(uploadService)),
          ChangeNotifierProvider(create: (_) => AccountController()),
          ChangeNotifierProvider(create: (_) => UploadSuccessController()),
          ChangeNotifierProvider(create: (_) => ExploreController(songService)),
          ChangeNotifierProvider(create: (_) => ServerStatusController(healthService)),
          ChangeNotifierProvider(create: (_) => LoginController(authService)),
          ChangeNotifierProvider(create: (_) => RegisterController(userService)),

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


