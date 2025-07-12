
from typing import List, Optional
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository


class GetAllOrderItemsUsecase:
    
    def __init__(self, order_item_gateway: IOrderItemRepository):
        self.order_item_gateway = order_item_gateway
    
    @classmethod
    def build(cls, order_item_gateway: IOrderItemRepository) -> 'GetAllOrderItemsUsecase':
        return cls(order_item_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[OrderItemDTO]:
        order_items = self.order_item_gateway.get_all(include_deleted)
        return order_items
    