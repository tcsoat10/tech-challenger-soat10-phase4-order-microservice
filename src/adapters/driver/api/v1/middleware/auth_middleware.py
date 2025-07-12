from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.core.exceptions.utils import ErrorCode
from src.core.utils.jwt_util import JWTUtil
import logging

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_routes = [
            "/openapi.json",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/api/v1/auth/token",
            "/api/v1/health",
        ]
        if any(request.url.path.startswith(route) for route in open_routes):
            return await call_next(request)

        for route in request.app.router.routes:
            if (
                hasattr(route, "path")
                and hasattr(route, "methods")
                and route.path == request.url.path
                and request.method in route.methods
            ):
                if getattr(route.endpoint, "bypass_auth", False):
                    return await call_next(request)


        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": {
                        "code": ErrorCode.UNAUTHORIZED.value,
                        "message": ErrorCode.UNAUTHORIZED.description,
                        "details": "Missing Authorization header",
                    }
                },
            )

        try:
            token = token.split("Bearer ")[1]
            payload = JWTUtil.decode_token(token)
            request.state.user = payload
        except ValueError as e:
            logging.error(f"Unauthorized access: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": {
                        "code": ErrorCode.UNAUTHORIZED.value,
                        "message": ErrorCode.UNAUTHORIZED.description,
                        "details": e.detail.get('message', str(e)),
                    }
                },
            )
        except Exception as e:
            logging.error(f"Forbidden access: {e}")
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": {
                        "code": ErrorCode.FORBIDDEN.value,
                        "message": ErrorCode.FORBIDDEN.description,
                        "details": e.detail.get('message', str(e)),
                    }
                },
            )

        return await call_next(request)
