from fastapi import Request

from src.app.core.config import settings

def check_secret_key(secret_key: str) -> bool:
    return secret_key == settings.HERCULE_SECRET_KEY

def check_request_secret_key(request: Request) -> bool:
    secret_key = request.headers.get("X-Hercule-Secret-Key")
    if secret_key is None:
        return False
    return check_secret_key(secret_key)
