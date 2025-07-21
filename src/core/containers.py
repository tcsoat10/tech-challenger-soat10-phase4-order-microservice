from dependency_injector import containers, providers

from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driver.api.v1.controllers.order_status_controller import OrderStatusController
from src.adapters.driver.api.v1.controllers.webhook_controller import WebhookController
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driver.api.v1.controllers.order_controller import OrderController
from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from src.adapters.driver.api.v1.controllers.order_item_controller import OrderItemController
from src.adapters.driven.providers.stock_provider.stock_microservice_gateway import StockMicroserviceGateway
from src.adapters.driven.providers.payment_provider.payment_provider_gateway import PaymentProviderGateway

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.order_status_controller",
        "src.adapters.driver.api.v1.routes.order_status_routes",
        "src.adapters.driver.api.v1.controllers.order_controller",
        "src.adapters.driver.api.v1.routes.order_routes",
        "src.adapters.driver.api.v1.controllers.order_item_controller",
        "src.adapters.driver.api.v1.routes.order_item_routes",
        "src.adapters.driver.api.v1.controllers.webhook_controller",
        "src.adapters.driven.providers.stock_provider.stock_microservice_gateway",
        "src.adapters.driven.providers.payment_provider.payment_provider_gateway",
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    stock_provider_gateway = providers.Singleton(StockMicroserviceGateway)
    payment_provider_gateway = providers.Singleton(PaymentProviderGateway)


    order_status_gateway = providers.Factory(OrderStatusRepository, db_session=db_session)
    order_status_controller = providers.Factory(OrderStatusController, order_status_gateway=order_status_gateway)

    order_gateway = providers.Factory(OrderRepository, db_session=db_session)
    order_controller = providers.Factory(
        OrderController,
        order_gateway=order_gateway,
        order_status_gateway=order_status_gateway,
        stock_gateway=stock_provider_gateway,
        payment_gateway=payment_provider_gateway
    )

    webhook_controller = providers.Factory(
        WebhookController,
        order_gateway=order_gateway,
        order_status_gateway=order_status_gateway,
        payment_gateway=payment_provider_gateway
    )

    order_item_gateway = providers.Factory(OrderItemRepository, db_session=db_session)
    order_item_controller = providers.Factory(
        OrderItemController,
        order_item_gateway=order_item_gateway,
        order_gateway=order_gateway,
        stock_gateway=stock_provider_gateway
    )
