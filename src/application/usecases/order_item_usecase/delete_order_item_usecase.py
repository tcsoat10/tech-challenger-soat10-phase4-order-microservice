
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository


class DeleteOrderItemUseCase:
    def __init__(self, order_item_gateway: IOrderItemRepository):
        self.order_item_gateway = order_item_gateway
    
    @classmethod
    def build(cls, order_item_gateway: IOrderItemRepository) -> 'DeleteOrderItemUseCase':
        return cls(order_item_gateway)

    def execute(self, order_item_id: int) -> None:
        order_item = self.order_item_gateway.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")
        
        if DELETE_MODE == 'soft':
            if order_item.is_deleted():
                raise EntityNotFoundException(entity_name="Order Item")

            order_item.soft_delete()
            self.order_item_gateway.update(order_item)
        else:
            self.order_item_gateway.delete(order_item)
