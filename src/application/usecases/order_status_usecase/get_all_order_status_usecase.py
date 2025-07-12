
from typing import List, Optional
from src.core.domain.entities.order_status import OrderStatus
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class GetAllOrderStatusUseCase:
    
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
        
    @classmethod
    def build(cls, order_status_gateway: IOrderStatusRepository):
        return cls(order_status_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[OrderStatus]:
        order_status = self.order_status_gateway.get_all(include_deleted=include_deleted)
        return order_status
