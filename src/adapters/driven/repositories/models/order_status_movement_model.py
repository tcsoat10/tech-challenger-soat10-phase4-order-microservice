from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.order import OrderStatusMovement
from src.core.shared.identity_map import IdentityMap

class OrderStatusMovementModel(BaseModel):
    __tablename__ = 'order_status_movements'

    id_order: Mapped[int] = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship('OrderModel', back_populates='status_history')

    order_snapshot: Mapped[dict] = Column(JSON, nullable=False, default=[])
    
    old_status: Mapped[Optional[str]] = Column(String(100), nullable=True)
    new_status: Mapped[str] = Column(String(100), nullable=False)

    changed_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False
    )
    changed_by: Mapped[str] = Column(String(300), nullable=True)
    
    @classmethod
    def from_entity(cls, movement: OrderStatusMovement) -> 'OrderStatusMovementModel':
        return cls(
            id_order=movement.order.id,
            order_snapshot=movement.order_snapshot,
            old_status=movement.old_status,
            new_status=movement.new_status,
            changed_at=movement.changed_at,
            changed_by=movement.changed_by,
            created_at=movement.created_at,
            updated_at=movement.updated_at,
            inactivated_at=movement.inactivated_at,
        )
        
    def to_entity(self) -> OrderStatusMovement:
        identity_map: IdentityMap = IdentityMap.get_instance()
        if existing_movement := identity_map.get(OrderStatusMovement, self.id):
            return existing_movement
        
        order = self._get_order(identity_map)
        movement = OrderStatusMovement(
            id=self.id,
            order=order,
            order_snapshot=self.order_snapshot,
            old_status=self.old_status,
            new_status=self.new_status,
            changed_at=self.changed_at,
            changed_by=self.changed_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
        )
        identity_map.add(movement)
        return movement
    
    def _get_order(self, identity_map: IdentityMap):
        from src.core.domain.entities.order import Order
        
        if existing_order := identity_map.get(Order, self.id_order):
            return existing_order
        return self.order.to_entity()
  
    
__all__ = ['OrderStatusMovementModel']    
