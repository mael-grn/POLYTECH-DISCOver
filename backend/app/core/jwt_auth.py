from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from flask import current_app

# Nom du cookie
COOKIE_NAME = "access_token"

def create_access_token(*, user_id: int) -> str:
    """
    Création d'un token d'accès JWT pour un utilisateur donné.

    - user_id : identifiant de l'utilisateur pour lequel le token est généré
    - retourne : token JWT en chaîne
    """
    # Date du moment
    now = datetime.now(timezone.utc)
    # Date d'expiration
    exp = now + timedelta(seconds=int(current_app.config["JWT_EXP_SECONDS"]))

    # Données stockées dans la clé
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    # Retour de la clé encodée
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm=current_app.config.get("JWT_ALG", "HS256"),
    )

def verify_access_token(token: str) -> int | None:
    """
    Vérification et décodage d'un token JWT pour récupérer l'identifiant utilisateur.

    - token: chaîne JWT
    - retourne:
        - l'identifiant utilisateur entier si le token est valide
        - None si le token est invalide, expiré ou si une erreur survient
    """
    try:
        # Vérification validité et signature du token
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=[current_app.config.get("JWT_ALG", "HS256")],
        )
        # Retour des données décodées
        return int(payload["sub"])
    # Si une erreur se produit, arrête la fonction    
    except Exception:
        return None
