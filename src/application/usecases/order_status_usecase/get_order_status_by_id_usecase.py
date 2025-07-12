
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class GetOrderStatusByIdUseCase:
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_status_gateway: IOrderStatusRepository) -> 'GetOrderStatusByIdUseCase':
        return cls(order_status_gateway)

    def execute(self, order_status_id: int) -> OrderStatus:
        order_status = self.order_status_gateway.get_by_id(order_status_id=order_status_id)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")

        return order_status
