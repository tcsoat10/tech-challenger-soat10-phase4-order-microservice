from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.entities.order import Order


class IOrderRepository(ABC):
    
    @abstractmethod
    def create(order: Order):
        pass

    @abstractmethod
    def get_by_customer_id(self, id_customer: int) -> List[Order]:
        pass

    @abstractmethod
    def get_by_employee_id(self, id_employee: int) -> List[Order]:
        pass
    
    @abstractmethod
    def get_by_payment_id(self, id_payment: int) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def get_all(self, status: Optional[List[str]], customer_id: Optional[int], include_deleted: Optional[bool]) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete(self, order: int) -> Order:
        pass
