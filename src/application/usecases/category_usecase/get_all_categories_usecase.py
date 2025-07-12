
from typing import List, Optional
from src.core.domain.entities.category import Category
from src.core.ports.category.i_category_repository import ICategoryRepository


class GetAllCategoriesUseCase:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway = category_gateway
        
    @classmethod
    def build(cls, category_gateway: ICategoryRepository):
        return cls(category_gateway)

    def execute(self, include_deleted: Optional[bool] = False) -> List[Category]:
        categories = self.category_gateway.get_all(include_deleted=include_deleted)
        return categories
