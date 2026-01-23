class User {
  final int id;
  final String firstName;
  final String lastName;
  final String email;

  const User(this.id, this.firstName, this.lastName, this.email);

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      json['user_id'],
      json['first_name'],
      json['last_name'],
      json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': id,
      'first_name': firstName,
      'last_name': lastName,
      'email': email,
    };
  }
}