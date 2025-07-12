
from src.core.domain.entities.category import Category
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.category.i_category_repository import ICategoryRepository


class GetCategoryByIdUseCase:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway = category_gateway

    @classmethod
    def build(cls, category_repository: ICategoryRepository):
        return cls(category_repository)

    def execute(self, category_id: int) -> Category:
        category = self.category_gateway.get_by_id(category_id=category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        
        return category
