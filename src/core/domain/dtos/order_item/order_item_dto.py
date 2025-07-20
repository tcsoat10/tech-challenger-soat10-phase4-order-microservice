from pydantic import BaseModel

from src.core.domain.entities.order_item import OrderItem

class OrderItemDTO(BaseModel):
    id: int
    product_name: str
    product_sku: str
    product_id: int | str
    product_category_name: str
    product_price: float
    quantity: int
    observation: str
    total: float

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> "OrderItemDTO":
        return cls(
            id=order_item.id,
            # order=OrderDTO.from_entity(order_item.order),
            product_name=order_item.product_name,
            product_sku=order_item.product_sku,
            product_id=order_item.product_id,
            product_category_name=order_item.product_category_name,
            product_price=order_item.product_price,
            quantity=order_item.quantity,
            observation=order_item.observation,
            total=order_item.total,
        )