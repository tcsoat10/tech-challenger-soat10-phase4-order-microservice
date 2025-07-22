from fastapi import Depends
from fastapi.security import SecurityScopes
from src.core.exceptions.forbidden_exception import ForbiddenException
from src.core.utils.jwt_util import JWTUtil
from src.core.auth.oauth2 import oauth2_scheme

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    payload = JWTUtil.decode_token(token)
    permissions = payload.get("profile", {}).get("permissions", [])

    for scope in security_scopes.scopes:
        if scope not in permissions:
            raise ForbiddenException("Forbidden access")

    return payload
