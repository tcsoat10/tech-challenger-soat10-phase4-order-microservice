
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class CreateOrderStatusUseCase:
    
    def __init__(self, order_status_gateway: IOrderStatusRepository):
        self.order_status_gateway = order_status_gateway
    
    @classmethod
    def build(self, order_status_gateway: IOrderStatusRepository) -> 'CreateOrderStatusUseCase':
        return CreateOrderStatusUseCase(order_status_gateway)
    
    def execute(self, dto: CreateOrderStatusDTO) -> OrderStatus:
        order_status = self.order_status_gateway.get_by_status(dto.status)
        if order_status:
            if not order_status.is_deleted():
                raise EntityDuplicatedException("OrderStatus")

            order_status.status = dto.status
            order_status.description = dto.description
            order_status.reactivate()
            self.order_status_gateway.update(order_status)
        else:
            order_status = OrderStatus(status=dto.status, description=dto.description)
            order_status = self.order_status_gateway.create(order_status)

        return order_status
