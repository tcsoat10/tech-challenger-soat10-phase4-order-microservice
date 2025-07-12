from dependency_injector import containers, providers

from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.adapters.driver.api.v1.controllers.category_controller import CategoryController
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driver.api.v1.controllers.product_controller import ProductController
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driver.api.v1.controllers.order_status_controller import OrderStatusController
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driver.api.v1.controllers.order_controller import OrderController
from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from src.adapters.driver.api.v1.controllers.order_item_controller import OrderItemController


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.category_controller",
        "src.adapters.driver.api.v1.controllers.product_controller",
        "src.adapters.driver.api.v1.controllers.order_status_controller",
        "src.adapters.driver.api.v1.routes.order_status_routes",
        "src.adapters.driver.api.v1.controllers.order_controller",
        "src.adapters.driver.api.v1.routes.order_routes",
        "src.adapters.driver.api.v1.controllers.order_item_controller",
        "src.adapters.driver.api.v1.routes.order_item_routes",
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    category_gateway = providers.Factory(
        CategoryRepository,
        db_session=db_session
    )

    category_controller = providers.Factory(
        CategoryController,
        category_gateway=category_gateway
    )

    product_gateway = providers.Factory(ProductRepository, db_session=db_session)
    product_controller = providers.Factory(
        ProductController, product_gateway=product_gateway, category_gateway=category_gateway
    )

    order_status_gateway = providers.Factory(OrderStatusRepository, db_session=db_session)
    order_status_controller = providers.Factory(OrderStatusController, order_status_gateway=order_status_gateway)

    order_gateway = providers.Factory(OrderRepository, db_session=db_session)
    order_controller = providers.Factory(
        OrderController,
        order_gateway=order_gateway,
        order_status_gateway=order_status_gateway,
        product_gateway=product_gateway
    )

    order_item_gateway = providers.Factory(OrderItemRepository, db_session=db_session)
    order_item_controller = providers.Factory(
        OrderItemController,
        order_item_gateway=order_item_gateway,
        order_gateway=order_gateway,
        product_gateway=product_gateway
    )    
