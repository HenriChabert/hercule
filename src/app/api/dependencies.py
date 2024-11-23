from fastapi import Depends, Security, HTTPException, status
from fastapi.security import APIKeyHeader

from src.app.core.security import check_secret_key

header_scheme = APIKeyHeader(name="X-Hercule-Secret-Key")

def check_secret_key_header(secret_key: str = Depends(header_scheme)):
    if not check_secret_key(secret_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret key")
    return True