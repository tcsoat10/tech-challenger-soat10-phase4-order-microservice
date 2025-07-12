from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.order_item import OrderItem


class IOrderItemRepository(ABC):
    
    @abstractmethod
    def create(order_item: OrderItem):
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: int, include_deleted: bool = False) -> List[OrderItem]:
        pass

    @abstractmethod
    def get_by_product_name(self, order_id: int, product_name: str) -> OrderItem:
        pass

    @abstractmethod
    def get_by_id(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[OrderItem]:
        pass

    @abstractmethod
    def update(self, order_item: OrderItem) -> OrderItem:
        pass
    
    @abstractmethod
    def delete(self, order_item: OrderItem) -> None:
        pass


__all__ = ["IOrderItemRepository"]
