from src.core.domain.entities.base_entity import BaseEntity
from datetime import datetime
from typing import Optional

class Category(BaseEntity):

    def __init__(
        self,
        name: str,
        description: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ) -> None:
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._description = description

    @classmethod
    def build(cls, name: str, description: str) -> "Category":
        return cls(name, description)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description
