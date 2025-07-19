
from src.core.domain.entities.order import Order
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway


class AddOrderItemInOrderUseCase:
    def __init__(self, order_gateway: IOrderRepository, stock_gateway: IStockProviderGateway):
        self.order_gateway = order_gateway
        self.stock_gateway = stock_gateway

    @classmethod
    def build(
        cls, order_gateway: IOrderRepository, stock_gateway: IStockProviderGateway
    ) -> 'AddOrderItemInOrderUseCase':
        return cls(order_gateway, stock_gateway)

    def execute(self, order_id: int, order_item_dto: dict) -> Order:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        item = self.stock_gateway.get_product_by_id(order_item_dto.product_id)
        if not item:
            raise EntityNotFoundException(f"Product ID '{order_item_dto.product_id}'")
        
        order_item = OrderItem(
            order=order,
            product_id=item.product_id,
            quantity=order_item_dto.quantity,
            observation=order_item_dto.observation,
            product_category_name=item.product_category_name
        )
        order.add_item(order_item)

        updated_order = self.order_gateway.update(order)
        return updated_order
