class User {
  final int id;
  final String name;
  final String email;

  const User(this.id, this.name, this.email);

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      json['user_id'],
      json['name'],
      json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': id,
      'name': name,
      'email': email,
    };
  }
}