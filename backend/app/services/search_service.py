import re
from sqlalchemy import or_, and_

def apply_rich_search(query, search: str, columns, mode: str = "any", max_tokens: int = 6):
    """
    Ajoute un filtre de recherche riche sur une query SQLAlchemy.

    - search: string utilisateur ("test song")
    - columns: liste de colonnes SQLAlchemy (ex: [Song.song_name, Song.artist_name])
    - mode:
        - "any" => OR entre tokens
        - "all" => AND entre tokens
    """
    # Récupération des tokens (morceau de texte)
    tokens = [t for t in re.split(r"\s+", (search or "").strip()) if t]
    # S'il n'y a pas de token, retourne la requête
    if not tokens:
        return query

    # Si le nombre de token dépasse le nombre maximal, couper les tokens jusqu'à ce qu'ils ne dépassent plus le nombre paximal
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]

    # Création du tableau contenant toutes les conditions de requête pour chaque token
    per_token = []
    # Boucle sur chaque token
    for tok in tokens:
        # Fait en sorte qu'un token puisse apparaître à n'importe quel moment dans le titre
        like = f"%{tok}%"
        # Ajoute la condition précédente au tableau
        per_token.append(or_(*[col.ilike(like) for col in columns]))

    # Retourne la requête filtrée pour tous les token si le mode est "all", sinon par token si le mode est "any"
    return query.filter(and_(*per_token)) if mode == "all" else query.filter(or_(*per_token))
