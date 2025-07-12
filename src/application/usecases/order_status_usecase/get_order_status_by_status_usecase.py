
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class GetOrderStatusByStatusUseCase:
    
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
    
    @classmethod
    def build(cls, order_status_gateway: IOrderStatusRepository) -> 'GetOrderStatusByStatusUseCase':
        return cls(order_status_gateway)
    
    def execute(self, status: str) -> OrderStatus:
        order_status = self.order_status_gateway.get_by_status(status=status)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        
        return order_status
