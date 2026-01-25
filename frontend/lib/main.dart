import 'package:discover/controllers/AccountController.dart';
import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/controllers/settings/EditUserDataController.dart';
import 'package:discover/controllers/settings/ManageUploadsController.dart';
import 'package:discover/controllers/settings/ViewUserDataController.dart';
import 'package:discover/controllers/song/SearchSongController.dart';
import 'package:discover/controllers/HomeController.dart';
import 'package:discover/controllers/upload/UploadController.dart';
import 'package:discover/controllers/upload/UploadSuccessController.dart';
import 'package:discover/services/AuthService.dart';
import 'package:discover/services/HealthService.dart';
import 'package:discover/services/SongService.dart';
import 'package:discover/services/UploadService.dart';
import 'package:discover/services/UserService.dart';
import 'package:discover/views/GlobalLayout.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'controllers/auth/LoginController.dart';
import 'controllers/auth/RegisterController.dart';
import 'controllers/settings/ServerStatusController.dart';
import 'core/global.dart';
import 'core/theme/app_theme.dart';

void main() async {

  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent, // Couleur de fond de la barre d'état
    statusBarIconBrightness: Brightness.dark, // Pour des icônes noires sur fond clair
  ));

  final uploadService = Uploadservice();
  final songService = SongService();
  final healthService = Healthservice();
  final userService = UserService();
  final authService = AuthService();


  runApp(
    MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => HomeController(uploadService, songService)),
          ChangeNotifierProvider(create: (_) => SearchSongController(songService)),
          ChangeNotifierProvider(create: (_) => UploadController(uploadService)),
          ChangeNotifierProvider(create: (_) => AccountController()),
          ChangeNotifierProvider(create: (_) => UploadSuccessController()),
          ChangeNotifierProvider(create: (_) => ExploreController(songService)),
          ChangeNotifierProvider(create: (_) => ServerStatusController(healthService)),
          ChangeNotifierProvider(create: (_) => LoginController(authService)),
          ChangeNotifierProvider(create: (_) => RegisterController(userService)),
          ChangeNotifierProvider(create: (_) => EditUserDataController(userService, authService)),
          ChangeNotifierProvider(create: (_) => ViewUserDataController(authService)),
          ChangeNotifierProvider(create: (_) => ManageUploadsController(uploadService)),

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


