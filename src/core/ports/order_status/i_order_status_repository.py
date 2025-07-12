from abc import ABC, abstractmethod

from src.core.domain.entities.order_status import OrderStatus


class IOrderStatusRepository(ABC):
    
    @abstractmethod
    def create(order: OrderStatus):
        pass

    @abstractmethod
    def exists_by_status(self, status: str) -> bool:
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> OrderStatus:
        pass

    @abstractmethod
    def get_by_id(self, order_status_id: int) -> OrderStatus:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> OrderStatus:
        pass

    @abstractmethod
    def update(self, order_status: OrderStatus) -> OrderStatus:
        pass

    @abstractmethod
    def delete(self, order_status: OrderStatus) -> OrderStatus:
        pass
