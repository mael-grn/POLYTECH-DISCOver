from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from flask import current_app

COOKIE_NAME = "access_token"

def create_access_token(*, user_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=int(current_app.config["JWT_EXP_SECONDS"]))

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm=current_app.config.get("JWT_ALG", "HS256"),
    )

def verify_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=[current_app.config.get("JWT_ALG", "HS256")],
        )
        return int(payload["sub"])
    except Exception:
        return None
