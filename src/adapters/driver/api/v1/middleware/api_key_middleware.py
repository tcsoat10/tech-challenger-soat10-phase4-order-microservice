import os
from typing import Callable, List
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match

class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Middleware para validar a chave de API (x-api-key) apenas em rotas específicas."""

    INCLUDED_PATHS: List[str] = [
        "/webhook/payment_notification",
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path not in self.INCLUDED_PATHS:
            return await call_next(request)

        # Verifica se a rota atual deve ignorar a autenticação por chave de API
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                if hasattr(route.endpoint, 'bypass_auth'):
                    return await call_next(request)
                break

        order_microservice_x_api_key = os.getenv("ORDER_MICROSERVICE_X_API_KEY")
        api_key = request.headers.get("x-api-key")

        if not order_microservice_x_api_key:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error: API Key not configured on server."}
            )

        if not api_key or api_key != order_microservice_x_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"}
            )

        return await call_next(request)