from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.entities.product import Product


class IProductRepository(ABC):
    
    @abstractmethod
    def create(product: Product):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def get_all(self, categories: Optional[List[str]], include_deleted: Optional[bool] = False) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def delete(self, product: Product) -> None:
        pass


__all__ = ["IProductRepository"]
