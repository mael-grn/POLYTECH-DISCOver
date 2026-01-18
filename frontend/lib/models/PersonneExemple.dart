class PersonneExemple {

  final String nom;
  final String prenom;
  final int id;

  const PersonneExemple(this.id, this.nom, this.prenom);

  factory PersonneExemple.fromJson(Map<String, dynamic> json) {
    return PersonneExemple(
      json['id'],
      json['nom'],
      json['prenom'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nom': nom,
      'prenom': prenom,
    };
  }
}