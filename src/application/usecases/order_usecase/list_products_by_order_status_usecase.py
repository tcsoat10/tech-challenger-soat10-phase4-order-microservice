
from typing import Any, Dict, List
from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway
from src.constants.order_status import OrderStatusEnum
from src.constants.product_category import ProductCategoryEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository


class ListProductsByOrderStatusUseCase:
    def __init__(self, order_gateway: IOrderRepository, stock_provider_gateway: IStockProviderGateway):
        self.order_gateway = order_gateway
        self.stock_provider_gateway = stock_provider_gateway

    @classmethod
    def build(cls, order_gateway: IOrderRepository, stock_provider_gateway: IStockProviderGateway) -> 'ListProductsByOrderStatusUseCase':
        return cls(order_gateway, stock_provider_gateway)

    def execute(self, order_id: int) -> List[Dict[str, Any]]:
        order = self.order_gateway.get_by_id(order_id)
        if order is None:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        '''
        profile_name = current_user.get('profile', {}).get('name')
        person_id = current_user.get('person', {}).get('id')
        if profile_name in ['customer', 'anonymous'] and order.customer.id != int(person_id or 0):
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        '''
        order_status = order.order_status.status
        status_category_map = {
            OrderStatusEnum.ORDER_WAITING_BURGERS.status: ProductCategoryEnum.BURGERS.name,
            OrderStatusEnum.ORDER_WAITING_SIDES.status: ProductCategoryEnum.SIDES.name,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status: ProductCategoryEnum.DRINKS.name,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status: ProductCategoryEnum.DESSERTS.name,
        }

        category = status_category_map.get(order_status)
        if category is None:
            raise BadRequestException("Não existem produtos disponíveis para este status de pedido.")

        category = self.stock_provider_gateway.get_category_by_name(category)
        if not category:
            raise EntityNotFoundException(message=f"Categoria '{category}' não encontrada.")

        products = self.stock_provider_gateway.get_products_by_category_id(category['id'])

        return products
