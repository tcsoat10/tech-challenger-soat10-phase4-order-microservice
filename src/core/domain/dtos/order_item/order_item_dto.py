from pydantic import BaseModel

from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.domain.entities.order_item import OrderItem

class OrderItemDTO(BaseModel):
    id: int
    product: ProductDTO
    quantity: int
    observation: str
    total: float

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> "OrderItemDTO":
        return cls(
            id=order_item.id,
            # order=OrderDTO.from_entity(order_item.order),
            product=ProductDTO.from_entity(order_item.product),
            quantity=order_item.quantity,
            observation=order_item.observation,
            total=order_item.total,
        )