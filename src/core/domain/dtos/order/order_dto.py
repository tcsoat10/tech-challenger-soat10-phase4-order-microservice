from typing import List, Optional
from pydantic import BaseModel
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.entities.order import Order

class OrderDTO(BaseModel):
    id: int
    customer: str
    order_status: OrderStatusDTO
    employee: Optional[str] = None
    order_items: Optional[List[OrderItemDTO]] = None

    @classmethod
    def from_entity(cls, order: Order) -> "OrderDTO":
        return cls(
            id = order.id,
            customer = order.id_customer,
            order_status = OrderStatusDTO.from_entity(order.order_status),
            employee = order.id_employee if order.id_employee else None,
            order_items = [OrderItemDTO.from_entity(item) for item in order.order_items]
        )
