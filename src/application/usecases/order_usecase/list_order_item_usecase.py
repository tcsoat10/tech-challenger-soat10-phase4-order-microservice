
from typing import List

from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository


class ListOrderItemsUseCase:
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository) -> 'ListOrderItemsUseCase':
        return cls(order_gateway)
    
    def execute(self, order_id: int) -> List[OrderItem]:
        order = self.order_gateway.get_by_id(order_id)
        if order is None:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        return order.list_order_items()
        
