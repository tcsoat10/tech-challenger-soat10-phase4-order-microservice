
from src.core.domain.entities.order import Order
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository


class GetOrderByIdUseCase:
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway

    @staticmethod
    def build(order_gateway: IOrderRepository):
        return GetOrderByIdUseCase(order_gateway)

    def execute(self, order_id: int, current_user: dict) -> Order:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if current_user['profile']['name'] in ['customer', 'anonymous'] and order.id_customer != current_user['person']['id']:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        return order
