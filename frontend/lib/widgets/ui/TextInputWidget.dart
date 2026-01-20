import 'package:discover/core/theme/app_theme.dart';
import 'package:flutter/material.dart';

class TextInputWidget extends StatelessWidget {
  final String? hint;
  final TextEditingController controller;
  final IconData? icon;
  final VoidCallback? onIconClick;
  final bool big;
  final ValueChanged<String>? onSubmitted;

  const TextInputWidget({
    this.hint,
    required this.controller,
    this.icon,
    this.onIconClick,
    this.big = false,
    this.onSubmitted,
    super.key
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 800,
      child: TextField(
        controller: controller,
        onChanged: (_) {
          if (onSubmitted != null) {
            onSubmitted!(controller.text);
          }
        },
        cursorColor: Colors.white,
        style: TextStyle(
          fontWeight: big ? FontWeight.w700 : FontWeight.w500,
          color: Colors.white,
          fontSize: big ? 22 : 17,
        ),
        selectionControls: materialTextSelectionControls, // par défaut
        decoration: InputDecoration(
          filled: true,
          fillColor: secondaryColor, // violet existant
          hintText: hint,
          hintStyle: TextStyle(color: Colors.white.withOpacity(0.8)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          suffixIcon: icon != null
              ? IconButton(
            icon: Icon(icon, color: Colors.white, size: big ? 35 : 25),
            onPressed: onIconClick,
          )
              : null,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50),
            borderSide: BorderSide.none,
          ),
        ),
      ),
    );
  }
}
