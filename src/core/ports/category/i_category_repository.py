from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.category import Category


class ICategoryRepository(ABC):
    
    @abstractmethod
    def create(category: Category):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Category:
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Category:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, category: Category) -> None:
        pass
