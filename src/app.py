from fastapi import FastAPI
from config.custom_openapi import custom_openapi
from src.adapters.driver.api.v1.middleware.api_key_middleware import ApiKeyMiddleware
from src.adapters.driver.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.core.containers import Container
from src.adapters.driver.api.v1.middleware.auth_middleware import AuthMiddleware
from src.adapters.driver.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.adapters.driver.api.v1.routes.health_check import router as health_check_router
from src.adapters.driver.api.v1.routes.order_item_routes import router as order_item_routes
from src.adapters.driver.api.v1.routes.order_status_routes import router as order_status_routes
from src.adapters.driver.api.v1.routes.order_routes import router as order_routes
from src.adapters.driver.api.v1.routes.webhook_routes import router as webhook_routes


app = FastAPI(title="Tech Challenger SOAT10 - FIAP")


# Inicializando o container de dependências
container = Container()
app.container = container

app.openapi = lambda: custom_openapi(app)

app.add_middleware(CustomErrorMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(IdentityMapMiddleware)
app.add_middleware(ApiKeyMiddleware)

# Adicionando rotas da versão 1
app.include_router(health_check_router, prefix="/api/v1")
app.include_router(order_routes, prefix="/api/v1", tags=["order"])
app.include_router(order_item_routes, prefix="/api/v1", tags=["order-items"], include_in_schema=False)
app.include_router(order_status_routes, prefix="/api/v1", tags=["order-status"])
app.include_router(webhook_routes, prefix="/api/v1/webhooks", tags=["webhooks"], include_in_schema=False)
