import 'package:discover/core/theme/app_theme.dart';
import 'package:flutter/material.dart';

class TextInputWidget extends StatelessWidget {
  final String? hint;
  final TextEditingController controller;
  final IconData? icon;
  final VoidCallback? onIconClick;
  final bool big;

  const TextInputWidget({
    this.hint,
    required this.controller,
    this.icon,
    this.onIconClick,
    this.big = false,
    super.key
  });

  @override
  Widget build(BuildContext context) {
    // Code couleur approximatif basé sur votre image (Bleu clair type "Periwinkle")
    const Color inputBackgroundColor = Color(0xFFA0C8FF);

    return TextField(
      controller: controller,
      cursorColor: Colors.white, // Curseur blanc pour aller avec le fond
      style: TextStyle(
        fontWeight: big ? FontWeight.w700 : FontWeight.w500,
        color: Colors.white, // Couleur du texte saisi
        fontSize: big ? 22 : 17,
      ),
      decoration: InputDecoration(
        // Active le remplissage de couleur
        filled: true,
        fillColor: secondaryColor,
        hintText: hint,
        hintStyle: TextStyle(color: Colors.white.withOpacity(0.8)),

        // Gestion de l'espacement interne pour que le texte ne colle pas aux bords
        contentPadding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),

        // L'icône est placée à droite (Suffix) et rendue cliquable
        suffixIcon: icon != null
            ? IconButton(
          icon: Icon(icon, color: Colors.white, size: big ? 35 : 25,),
          onPressed: onIconClick,
        )
            : null,

        // Bordure en état normal (repos)
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(50.0), // Rayon élevé pour la forme "pilule"
          borderSide: BorderSide.none, // Pas de trait de bordure
        ),

        // Bordure quand le champ est activé mais pas sélectionné (identique pour la cohérence)
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(50.0),
          borderSide: BorderSide.none,
        ),

        // Bordure quand on écrit dedans (Focus)
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(50.0),
          borderSide: BorderSide.none,
          // Vous pouvez ajouter une légère bordure blanche ici si vous voulez souligner le focus
        ),
      ),
    );
  }
}