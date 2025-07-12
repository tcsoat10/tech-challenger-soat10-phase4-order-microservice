from jose import jwt
from datetime import datetime, timedelta, timezone
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
from src.core.exceptions.invalid_token_exception import InvalidTokenException

class JWTUtil:
    @staticmethod
    def create_token(data: dict) -> str:
        payload = {
            **data,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.now(timezone.utc)
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if not payload:
                raise InvalidTokenException(message="Invalid token payload")
            return payload
        except jwt.ExpiredSignatureError:
                raise InvalidTokenException(message="Token has expired.")
        except jwt.InvalidTokenError:
                raise InvalidTokenException(message="Invalid token.")
