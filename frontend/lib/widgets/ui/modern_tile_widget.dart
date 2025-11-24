import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class ModernTileWidget extends StatelessWidget {
 final IconData icon;
 final String title;
 final VoidCallback onTap;
 final Color? iconColor;

  const ModernTileWidget({
    required this.icon,
    required this.title,
    required this.onTap,
    this.iconColor,
    super.key
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 0, vertical: 8),
      child: Material(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(18),
        elevation: 2,
        shadowColor: Colors.black12,
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 16),
            child: Row(
              children: [
                Icon(icon, color: iconColor ?? foregroundVariantColor, size: 28),
                const SizedBox(width: 18),
                Expanded(
                  child: Text(
                    title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                const Icon(Icons.chevron_right, color: secondaryColor, size: 26),
              ],
            ),
          ),
        ),
      ),
    );
  }
}