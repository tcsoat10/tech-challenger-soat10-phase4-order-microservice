from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.domain.entities.order_status import OrderStatus
from src.application.usecases.order_usecase.get_order_by_id_usecase import GetOrderByIdUseCase


class GetOrderStatusUsecase():
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway
    
    @classmethod
    def build(cls, order_gateway: IOrderRepository) -> 'GetOrderStatusUsecase':
        return GetOrderStatusUsecase(order_gateway)

    def execute(self, order_id: int, current_user: dict) -> OrderStatus:
        get_order_by_id_usecase = GetOrderByIdUseCase.build(self.order_gateway)
        
        order = get_order_by_id_usecase.execute(order_id, current_user)

        return order.order_status
        