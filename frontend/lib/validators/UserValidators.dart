class UserValidators {
  static String? emailValidator(String? value) {
    if (value == null || value.trim().isEmpty) {
      return "The email address is required";
    }
    final emailRegExp = RegExp(
      r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
    );
    if (!emailRegExp.hasMatch(value)) {
      return "Please enter a valid email address";
    }
    return null;
  }
  static String? passwordValidator(String? value) {
    if (value == null || value.isEmpty) {
      return "The password is required";
    }
    if (value.length < 6) {
      return "The password must be at least 6 characters long";
    }
    return null;
  }
  static String? nameValidator(String? value) {
    if (value == null || value.isEmpty) {
      return "The name is required";
    }
    if (value.length < 3) {
      return "The name must be at least 3 characters long";
    }
    return null;
  }
}