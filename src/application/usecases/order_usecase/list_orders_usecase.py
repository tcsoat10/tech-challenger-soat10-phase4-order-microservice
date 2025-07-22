
from typing import List
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from src.constants.order_status import OrderStatusEnum


class ListOrdersUseCase:
    
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository):
        return cls(order_gateway)

    def execute(self, status: List[str] = None, current_user: dict = {}) -> List[Order]:
        customer_id = current_user['person']['id'] if current_user.get('profile', {}).get('name') == 'customer' else None

        if status is None:
            status = [
                OrderStatusEnum.ORDER_PAID.status, # Order paid by the customer
                OrderStatusEnum.ORDER_PREPARING.status, # Order being prepared by the staff
                OrderStatusEnum.ORDER_READY.status # Order ready for pickup
            ]

        orders = self.order_gateway.get_all(status=status, customer_id=customer_id)
        return orders
