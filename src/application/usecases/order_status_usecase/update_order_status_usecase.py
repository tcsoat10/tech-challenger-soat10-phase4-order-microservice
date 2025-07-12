
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class UpdateOrderStatusUseCase:
    
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_status_gateway: IOrderStatusRepository):
        return cls(order_status_gateway)
    
    def execute(self, order_status_id: int, dto: UpdateOrderStatusDTO) -> OrderStatus:
        order_status = self.order_status_gateway.get_by_id(order_status_id)
        if not order_status:
            raise EntityDuplicatedException(entity_name="OrderStatus")
    
        order_status.status=dto.status
        order_status.description=dto.description
        
        order_status = self.order_status_gateway.update(order_status)

        return order_status
