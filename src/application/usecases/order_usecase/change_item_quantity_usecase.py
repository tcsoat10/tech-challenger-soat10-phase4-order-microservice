
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository


class ChangeItemQuantityUseCase:
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository) -> 'ChangeItemQuantityUseCase':
        return cls(order_gateway)
    
    def execute(self, order_id: int, order_item_id: int, new_quantity: int) -> None:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        order_item = next((order_item for order_item in order.order_items if order_item.id == order_item_id), None)
        if not order_item:
            raise EntityNotFoundException(message=f"O item com ID '{order_item_id}' não foi encontrado no pedido.")

        order.change_item_quantity(order_item, new_quantity)
        self.order_gateway.update(order)
        return None