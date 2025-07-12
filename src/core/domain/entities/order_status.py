from src.core.domain.entities.base_entity import BaseEntity
from typing import Optional
from datetime import datetime


class OrderStatus(BaseEntity):
    def __init__(
            self,
            status: str,
            description: str,
            id: Optional[int] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
            inactivated_at: Optional[datetime] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._status = status
        self._description = description
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
