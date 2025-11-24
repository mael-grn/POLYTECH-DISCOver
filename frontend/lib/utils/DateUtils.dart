class CustomDateUtils {

  static String getDateString(DateTime date) {
    Duration difference = DateTime.now().difference(date);

    if (difference.inMinutes < 1) {
      return "À l'instant";
    } else if (difference.inMinutes < 60) {
      return "Il y a ${difference.inMinutes} minutes";
    } else if (difference.inHours < 24) {
      return "Il y a ${difference.inHours} heures";
    } else if (difference.inDays < 7) {
      return "Il y a ${difference.inDays} jours";
    } else {
      // Format : 15 janvier
      List<String> months = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
      ];
      return "${date.day} ${months[date.month - 1]}";
    }
  }

}