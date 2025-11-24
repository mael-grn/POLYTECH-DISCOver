enum NetworkErrorEnum {
  unauthorized(401, 'Non autorisé'),
  paymentRequired(402, 'Paiement requis'),
  forbidden(403, 'Accès refusé'),
  notFound(404, 'Ressource non trouvée'),
  methodNotAllowed(405, 'Méthode non autorisée'),
  notAcceptable(406, 'Non acceptable'),
  proxyAuthenticationRequired(407, 'Authentification du proxy requise'),
  requestTimeout(408, 'Délai d\'attente de la requête expiré'),
  conflict(409, 'Conflit'),
  gone(410, 'Disparu'),
  lengthRequired(411, 'Longueur requise'),
  preconditionFailed(412, 'Précondition échouée'),
  payloadTooLarge(413, 'Charge utile trop volumineuse'),
  uriTooLong(414, 'URI trop longue'),
  unsupportedMediaType(415, 'Type de média non pris en charge'),
  rangeNotSatisfiable(416, 'Plage non satisfiable'),
  expectationFailed(417, 'Attente échouée'),
  imATeapot(418, 'Je suis une théière'), // RFC 2324
  misdirectedRequest(421, 'Requête mal dirigée'),
  unprocessableContent(422, 'Contenu non traitable'),
  locked(423, 'Verrouillé'),
  failedDependency(424, 'Dépendance échouée'),
  tooEarly(425, 'Trop tôt'),
  upgradeRequired(426, 'Mise à niveau requise'),
  preconditionRequired(428, 'Précondition requise'),
  tooManyRequests(429, 'Trop de requêtes'),
  requestHeaderFieldsTooLarge(431, 'Champs d\'en-tête de requête trop volumineux'),
  unavailableForLegalReasons(451, 'Indisponible pour des raisons légales'),

  internalServerError(500, 'Erreur interne du serveur'),
  notImplemented(501, 'Non implémenté'),
  badGateway(502, 'Mauvaise passerelle'),
  serviceUnavailable(503, 'Service temporairement indisponible'),
  gatewayTimeout(504, 'Délai d\'attente de la passerelle expiré'),
  httpVersionNotSupported(505, 'Version HTTP non prise en charge'),
  variantAlsoNegotiates(506, 'La variante négocie également'),
  insufficientStorage(507, 'Stockage insuffisant'),
  loopDetected(508, 'Boucle détectée'),
  notExtended(510, 'Non étendu'),
  networkAuthenticationRequired(511, 'Authentification réseau requise'),

  unknownError(-1, 'Erreur réseau inconnue'); // Pour les erreurs non standard ou inattendues

  final int code;
  final String message;

  const NetworkErrorEnum(this.code, this.message);

  static NetworkErrorEnum fromCode(int code) {
    return NetworkErrorEnum.values.firstWhere((error) => error.code == code, orElse: () => NetworkErrorEnum.unknownError);
  }
}