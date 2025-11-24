import 'package:flutter/material.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';
import 'package:discover/widgets/ui/button_widget.dart';

import '../core/theme/app_theme.dart';
import '../enums/NetworkErrorEnum.dart';
import '../main.dart';
import '../widgets/animations/scale_animation_widget.dart';

class DialogBuilder {
  static final context = navigatorKey.currentContext;
  static bool _isDialogOpen = false;

  static Future<void> _showDialog(Widget Function(BuildContext) builder) {
    if (context == null) {
      return Future.value();
    }
    if (_isDialogOpen) {
      closeCurrentDialog();
    }
    _isDialogOpen = true;
    return showDialog<void>(
      barrierDismissible: false,
      context: context!,
      builder: builder,
    );
  }

  static closeCurrentDialog() {
    if (context == null) {
      return;
    }
    if (_isDialogOpen) {
      Navigator.of(context!).pop();
      _isDialogOpen = false;
    }
  }

  static Future<void> _simpleImageDialog(
    String title,
    String content,
    String image, [
    Function? onCLose,
  ]) {
    return _showDialog((BuildContext context) {
      return ScaleAnimationWidget(
        child: AlertDialog(
          backgroundColor: backgroundVariantColor,
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Image.asset(width: 300, height: 200, image),
                SizedBox(height: 20),
                Text(
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
                  title,
                ),
                SizedBox(height: 20),
                Text(textAlign: TextAlign.center, content),
              ],
            ),
          ),

          actions: <Widget>[
            ButtonWidget(
                message: "Ok",
                icon: Icons.check,
                onPressed: () {
                  closeCurrentDialog();
                  if (onCLose != null) {
                    onCLose();
                  }
                }
            )
          ],
        )
      );
    });
  }

  static Future<void> success(
    String title,
    String content, {
        Function? onCLose,
      }) {
    return _simpleImageDialog(
      title,
      content,
      "images/thumbs_up.png",
      onCLose,
    );
  }

  static Future<void> warning(
    String title,
    String content, {
        Function? onCLose,
      }) {
    return _simpleImageDialog(
      title,
      content,
      "images/warning.png",
      onCLose,
    );
  }

  static Future<void> networkError(
    NetworkErrorEnum error, {
        List<
            ({int code, String title, String message})> personalizedErrors = const [
        ],
        Function? onCLose,
      }) {
    String image = "";
    String title = "Une erreur s'est produite lors de la connexion au serveur";
    String detailedMessage = "";
    switch (error) {
      case NetworkErrorEnum.unauthorized:
        detailedMessage =
            "Vous n'êtes pas autorisé à accéder à cette ressource. Veuillez vous connecter.";
        image = "images/bodyguard.png";
        break;
      case NetworkErrorEnum.forbidden:
        detailedMessage =
            "Accès refusé. Vous n'avez pas les autorisations nécessaires.";
        image = "images/bodyguard.png";
        break;
      case NetworkErrorEnum.notFound:
        detailedMessage =
            "La ressource demandée est introuvable. Verifiez les mises à jour de l'application.";
        image = "images/searching.png";
        break;
      case NetworkErrorEnum.requestTimeout:
        detailedMessage =
            "Le serveur a mis trop de temps à répondre. Veuillez réessayer plus tard.";
        image = "images/timer.png";
      case NetworkErrorEnum.internalServerError:
        detailedMessage =
            "Erreur interne du serveur. Veuillez réessayer plus tard.";
        image = "images/broken_server.png";
        break;
      case _:
        detailedMessage =
            "Une erreur s'est produite. Veuillez réessayer plus tard.";
        image = "images/broken_phone.png";
    }

    for (var e in personalizedErrors) {
      if (e.code == error.code) {
        title = e.title;
        detailedMessage = e.message;
      }
    }

    return _simpleImageDialog(
      title,
      "$detailedMessage (${error.code} : ${error.message})",
      image,
      onCLose,
    );
  }

  static Future<void> serverError({Function? onCLose}) {
    return _simpleImageDialog(
      "Erreur",
      "Une erreur s'est produite lors de la connexion aux serveurs. Veuillez réessayer plus tard",
      "images/broken_server.png",
      onCLose,
    );
  }

  static Future<void> appError({Function? onCLose}) {
    return _simpleImageDialog(
      "Erreur",
      "Une erreur s'est produite dans l'application. Essayez de verifier les mises à jours. Si le problème persiste, vous pouvez contacter le support.",
      "images/broken_phone.png",
      onCLose,
    );
  }

  static Future<void> error(String title, String content, {Function? onCLose}) {
    return _simpleImageDialog(
      title,
      content,
      "images/error.png",
      onCLose,
    );
  }

  static Future<void> loading() {
    return _showDialog((BuildContext context) {
      return AlertDialog(
        content: SizedBox(
          width: 100,
          height: 100,
          child: Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                LoadingAnimationWidget.inkDrop(
                  color: foregroundColor,
                  size: 30,
                ),
                const SizedBox(height: 20),
                const Text("Chargement..."),
              ],
            ),
          ),
        ),
      );
    });
  }

  static Future<void> customDialog(Widget content, List<Widget> actions) {
    return _showDialog((BuildContext context) {
      return AlertDialog(
        content: content,
        actions: actions,
      );
    });
  }

  static Future<void> selectGroupPicture(Function(String) setPicture) {
    final profilePictureList = [
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/beach-NW0LPttdoWxLlZzPgZVrhQAWCi84Vd.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/city-JTEWzXA2EUaOeOoYwJjQOqMgOqQJbx.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/club-9xv8vjhj3PThYL5SjjmKQp4YmUYhrI.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/earth-vW4z1540GtccjQ7c3uInL6shx5mHGB.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/hills-Ik4CBVlh2caJdP1BQlWu7EDwzXgXnH.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/mountains-L0MVW77mf9IvsyTV2RhYqZrdjl3PoZ.png"
    ];

    return _showDialog((BuildContext context) {
      String? selectedProfilePicture;
      return StatefulBuilder(
        builder: (context, setState) {
          return AlertDialog(
            title: Text(
              "Sélectionner une image de groupe",
              textAlign: TextAlign.center,
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 22),
            ),
            content: SizedBox(
              width: 350,
              child: GridView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                itemCount: profilePictureList.length,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  mainAxisSpacing: 16,
                  crossAxisSpacing: 16,
                  childAspectRatio: 1,
                ),
                itemBuilder: (context, index) {
                  final url = profilePictureList[index];
                  final isSelected = selectedProfilePicture == url;
                  return GestureDetector(
                    onTap: () {
                      setState(() {
                        selectedProfilePicture = url;
                      });
                    },
                    child: AnimatedScale(
                      scale: isSelected ? 0.85 : 1.0,
                      duration: Duration(milliseconds: 200),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          ClipOval(
                            child: Image.network(
                              url,
                              width: 80,
                              height: 80,
                              fit: BoxFit.cover,
                            ),
                          ),
                          if (isSelected)
                            Positioned(
                              right: 4,
                              top: 4,
                              child: Container(
                                decoration: BoxDecoration(
                                  color: secondaryColor,
                                  shape: BoxShape.circle,
                                ),
                                padding: EdgeInsets.all(4),
                                child: Icon(Icons.check, color: Colors.white, size: 18),
                              ),
                            ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            actions: [
              ButtonWidget(
                message: "Sélectionner",
                icon: Icons.check,
                onPressed: selectedProfilePicture == null
                    ? () {}
                    : () {
                  closeCurrentDialog();
                  setPicture(selectedProfilePicture!);
                },
                backgroundColor: selectedProfilePicture == null
                    ? Colors.grey
                    : secondaryColor,
              ),
            ],
          );
        },
      );
    });
  }

  static void datePicker(
    Function(DateTime) onDateSelected, {
    DateTime? initialDate,
  }) {
    showDatePicker(
      context: context!,
      initialDate: initialDate ?? DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime(2100),
    ).then((selectedDate) {
      if (selectedDate != null) {
        onDateSelected(selectedDate);
      }
    });
  }

  static Future<void> selectProfilePicture(Function(String) setPicture) {
    final profilePictureList = [
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/1-IvHGkdEmlE4R9xy8xxxHVBUD3R7Y4U.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/2-zJBSjydpEFU3fZyRx9OTaXjE2x4pwS.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/3-hhmhism9G9RGUOSxW8hpv1LAjkrMuV.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/4-RMemqi6ybWeMWG8tyceq3QbNUQL7hJ.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/5-RKMWbv7QktBuJwI4XlRMmNz4H6RmK6.png",
      "https://6q7xemamt4xekhet.public.blob.vercel-storage.com/6-vqXuNlcTnPomsvNBFCwBgaGH3jKCq6.png"
    ];

    return _showDialog((BuildContext context) {
      String? selectedProfilePicture;
      return StatefulBuilder(
        builder: (context, setState) {
          return AlertDialog(
            title: Text(
              "Sélectionner une image de groupe",
              textAlign: TextAlign.center,
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 22),
            ),
            content: SizedBox(
              width: 350,
              child: GridView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                itemCount: profilePictureList.length,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  mainAxisSpacing: 16,
                  crossAxisSpacing: 16,
                  childAspectRatio: 1,
                ),
                itemBuilder: (context, index) {
                  final url = profilePictureList[index];
                  final isSelected = selectedProfilePicture == url;
                  return GestureDetector(
                    onTap: () {
                      setState(() {
                        selectedProfilePicture = url;
                      });
                    },
                    child: AnimatedScale(
                      scale: isSelected ? 0.85 : 1.0,
                      duration: Duration(milliseconds: 200),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          ClipOval(
                            child: Image.network(
                              url,
                              width: 80,
                              height: 80,
                              fit: BoxFit.cover,
                            ),
                          ),
                          if (isSelected)
                            Positioned(
                              right: 4,
                              top: 4,
                              child: Container(
                                decoration: BoxDecoration(
                                  color: secondaryColor,
                                  shape: BoxShape.circle,
                                ),
                                padding: EdgeInsets.all(4),
                                child: Icon(Icons.check, color: Colors.white, size: 18),
                              ),
                            ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            actions: [
              ButtonWidget(
                message: "Sélectionner",
                icon: Icons.check,
                onPressed: selectedProfilePicture == null
                    ? () {}
                    : () {
                  closeCurrentDialog();
                  setPicture(selectedProfilePicture!);
                },
                backgroundColor: selectedProfilePicture == null
                    ? Colors.grey
                    : secondaryColor,
              ),
            ],
          );
        },
      );
    });
  }

  static Future<void> yesOrNo(
    String title,
    String content,
    Function onYes, {
        Function? onNo,
      }) {
    return _showDialog((BuildContext context) {
      return ScaleAnimationWidget(
          child: AlertDialog(
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Image.asset(width: 300, height: 200, "images/interrogation.png"),
                  SizedBox(height: 20),
                  Text(
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
                    title,
                  ),
                  SizedBox(height: 20),
                  Text(textAlign: TextAlign.center, content),
                ],
              ),
            ),

            actions: <Widget>[
              ButtonWidget(
                  message: "Non",
                  backgroundColor: Colors.redAccent,
                  icon: Icons.close,
                  onPressed: () {
                    closeCurrentDialog();
                    if (onNo != null) {
                      onNo();
                    }
                  }
              ),
              ButtonWidget(
                  message: "Oui",
                  icon: Icons.check,
                  onPressed: () {
                    closeCurrentDialog();
                    onYes();
                  }
              )
            ],
          )
      );
    });
  }
}
