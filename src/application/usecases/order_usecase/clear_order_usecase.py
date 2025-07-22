
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.order.i_order_repository import IOrderRepository


class ClearOrderUseCase:
    def __init__(self, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository):
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository) -> 'ClearOrderUseCase':
        return cls(order_gateway, order_status_gateway)
    
    def execute(self, order_id: int, current_user: dict) -> None:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if current_user['profile']['name'] in ['customer', 'anonymous'] and order.id_customer != current_user['person']['id']:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        order.clear_order(self.order_status_gateway)
        self.order_gateway.update(order)