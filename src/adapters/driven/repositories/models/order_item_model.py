from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.core.domain.entities.order_item import OrderItem
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.base_model import BaseModel


class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(ForeignKey("orders.id"), nullable=False)
    order = relationship("OrderModel", back_populates="order_items")

    product_id = Column(ForeignKey("products.id"), nullable=False)
    product = relationship("ProductModel")

    quantity = Column(Integer, nullable=False, default=1)

    observation = Column(String(300))
    
    @classmethod
    def from_entity(cls, order_item: OrderItem) -> "OrderItemModel":
        
        order_id = order_item.order.id if order_item.order else None
        product_id = order_item.product.id if order_item.product else None

        return cls(
            order_id=order_id,
            product_id=product_id,
            quantity=order_item.quantity,
            observation=order_item.observation,
            id=order_item.id,
            created_at=order_item.created_at,
            updated_at=order_item.updated_at,
            inactivated_at=order_item.inactivated_at,
        )
        
    def to_entity(self) -> OrderItem:
        identity_map: IdentityMap = IdentityMap.get_instance()
        if existing_order_item := identity_map.get(OrderItem, self.id):
            return existing_order_item

        order_item = OrderItem()
        identity_map.add(order_item)

        product = self._get_product(identity_map)
        order = self._get_order(identity_map)

        order_item.order = order
        order_item.product = product
        order_item.quantity = self.quantity
        order_item.observation = self.observation
        order_item.id = self.id
        order_item.created_at = self.created_at
        order_item.updated_at = self.updated_at
        order_item.inactivated_at = self.inactivated_at

        return order_item
        
    def _get_product(self, identity_map: IdentityMap):
        from src.core.domain.entities.product import Product
        if existing_product := identity_map.get(Product, self.product_id):
            return existing_product
        return self.product.to_entity() if self.product else None
    
    def _get_order(self, identity_map: IdentityMap):
        from src.core.domain.entities.order import Order
        if existing_order := identity_map.get(Order, self.order_id):
            return existing_order
        return self.order.to_entity() if self.order and self.order.id else None


__all__ = ["OrderItemModel"]
