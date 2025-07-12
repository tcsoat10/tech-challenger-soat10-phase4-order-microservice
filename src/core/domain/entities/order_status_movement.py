from typing import Optional
from datetime import datetime
from src.core.domain.entities.base_entity import BaseEntity

class OrderStatusMovement(BaseEntity):
    
    def __init__(
        self,
        old_status: Optional[str],
        new_status: str,
        changed_by: str,
        changed_at: datetime,
        order = None,
        order_snapshot: Optional[dict] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self.order = order
        self.order_snapshot = order_snapshot
        self.old_status = old_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.changed_at = changed_at
        
    # getters and setters
    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def order_snapshot(self):
        return self._order_snapshot

    @order_snapshot.setter
    def order_snapshot(self, value):
        self._order_snapshot = value

    @property
    def old_status(self):
        return self._old_status

    @old_status.setter
    def old_status(self, value):
        self._old_status = value

    @property
    def new_status(self):
        return self._new_status

    @new_status.setter
    def new_status(self, value):
        self._new_status = value

    @property
    def changed_by(self):
        return self._changed_by

    @changed_by.setter
    def changed_by(self, value):
        self._changed_by = value

    @property
    def changed_at(self):
        return self._changed_at

    @changed_at.setter
    def changed_at(self, value):
        self._changed_at = value

    def __str__(self):
        return (
            f"OrderStatusMovement(order={self.order}, order_snapshot={self.order_snapshot}, "
            f"old_status={self.old_status}, new_status={self.new_status}, "
            f"changed_by={self.changed_by}, changed_at={self.changed_at}, "
            f"id={self.id}, created_at={self.created_at}, updated_at={self.updated_at}, "
            f"inactivated_at={self.inactivated_at})"
        )


__all__ = ['OrderStatusMovement']
