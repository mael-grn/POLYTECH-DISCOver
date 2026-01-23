from flask import request
def get_request_user_id() -> int | None:
    """
    """
    raw = request.headers.get("X-User-Id") or request.args.get("user_id")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None