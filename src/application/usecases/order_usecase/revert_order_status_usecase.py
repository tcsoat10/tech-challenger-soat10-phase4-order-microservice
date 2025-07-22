
from src.constants.order_transition import STATUS_ALLOWED_ACCESS_ONLY_CUSTOMER
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class RevertOrderStatusUseCase:
    def __init__(self, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository):
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository) -> 'RevertOrderStatusUseCase':
        return cls(order_gateway, order_status_gateway)
    
    def execute(self, order_id: int, current_user: dict) -> Order:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if order.order_status in STATUS_ALLOWED_ACCESS_ONLY_CUSTOMER and current_user['profile']['name'] not in ['customer', 'anonymous']:
            raise BadRequestException("Você não tem permissão para avançar o pedido para o próximo passo.")

        order.revert_order_status(self.order_status_gateway)
        self.order_gateway.update(order)
        return order
