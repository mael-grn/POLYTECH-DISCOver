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
    tokens = [t for t in re.split(r"\s+", (search or "").strip()) if t]
    if not tokens:
        return query

    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]

    per_token = []
    for tok in tokens:
        like = f"%{tok}%"
        per_token.append(or_(*[col.ilike(like) for col in columns]))

    return query.filter(and_(*per_token)) if mode == "all" else query.filter(or_(*per_token))
