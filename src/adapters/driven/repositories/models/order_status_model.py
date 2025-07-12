from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.order_status import OrderStatus

from sqlalchemy import Column, String


class OrderStatusModel(BaseModel):
    __tablename__ = 'order_status'

    status = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            status=entity.status,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )
        
    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(OrderStatus, self.id)
        if existing:
            return existing
        
        order_status = OrderStatus(
            id=self.id,
            status=self.status,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(order_status)
        return order_status
        

__all__ = ['OrderStatusModel']
