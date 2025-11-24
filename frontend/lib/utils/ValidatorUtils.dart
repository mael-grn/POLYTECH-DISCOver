
class ValidatorUtils {

  static String? checkPrenomFormat(String? prenom) {

    if (prenom == null || prenom.isEmpty) {
      return "Il faut saisir quelque chose...";

    } else {
      return null;
    }
  }

}