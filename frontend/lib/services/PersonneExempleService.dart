import 'dart:convert';
import 'package:discover/models/PersonneExemple.dart';
import '../core/provider.dart';

class PersonneExampleService {

  Future<PersonneExemple> recupererPersonne() async {
    /*
    final response = await Provider.sendRequest(route: '/user', method: HttpMethod.GET);
    return PersonneExemple.fromJson(jsonDecode(response));

     */
    return PersonneExemple(1, "Garnier", "Mael");
  }

  Future<PersonneExemple> creerPersonne(String nom, String prenom) async {
    final response = await Provider.sendRequest(route: '/user', method: HttpMethod.POST, body: {
      "nom" : nom,
      "prenom" : prenom
    });
    return PersonneExemple.fromJson(jsonDecode(response));

  }

  Future<PersonneExemple> modifierPrenom(int id, String prenom) async {
    /*
    final response = await Provider.sendRequest(route: '/user', method: HttpMethod.PUT, body: {
      "prenom" : prenom
    });
    return PersonneExemple.fromJson(jsonDecode(response));

     */
    return PersonneExemple(id, "Garnier", prenom);
  }
}