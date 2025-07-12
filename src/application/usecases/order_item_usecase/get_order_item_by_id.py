from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository


class GetOrderItemByIdUseCase:
    def __init__(self, order_item_gateway: IOrderItemRepository):
        self.order_item_gateway = order_item_gateway

    @classmethod
    def build(cls, order_item_gateway: IOrderItemRepository) -> 'GetOrderItemByIdUseCase':
        return cls(order_item_gateway)
    
    def execute(self, order_item_id: int) -> OrderItem:
        order_item = self.order_item_gateway.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")
        
        return order_item
