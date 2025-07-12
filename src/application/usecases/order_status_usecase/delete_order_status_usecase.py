
from config.database import DELETE_MODE
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class DeleteOrderStatusUseCase:
    
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_status_gateway: IOrderStatusRepository) -> "DeleteOrderStatusUseCase":
        return cls(order_status_gateway)
    
    def execute(self, order_status_id: int) -> None:
        order_status: OrderStatus = self.order_status_gateway.get_by_id(order_status_id)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        
        if DELETE_MODE == 'soft':
            if order_status.is_deleted():
                raise EntityNotFoundException(entity_name="OrderStatus")

            order_status.soft_delete()
            self.order_status_gateway.update(order_status)
        else:
            self.order_status_gateway.delete(order_status)
