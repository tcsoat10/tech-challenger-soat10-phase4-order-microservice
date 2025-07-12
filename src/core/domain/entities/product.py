from typing import Optional
from src.core.domain.entities.category import Category
from src.core.domain.entities.base_entity import BaseEntity


class Product(BaseEntity):

    def __init__(
        self, 
        name: str, 
        description: str, 
        price: float,
        category: Category = None,
        sla_product: str = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None,
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._description = description
        self._category = category
        self._price = price
        self._sla_product = sla_product


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

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, category: Category) -> None:
        self._category = category

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._price = price

    @property
    def sla_product(self) -> Optional[str]:
        return self._sla_product

    @sla_product.setter
    def sla_product(self, sla_product: Optional[str]) -> None:
        self._sla_product = sla_product

__all__ = ["Product"]
