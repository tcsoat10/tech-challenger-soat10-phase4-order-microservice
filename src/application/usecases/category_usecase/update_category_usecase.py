
from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.core.domain.entities.category import Category
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.category.i_category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway = category_gateway
    
    @classmethod
    def build(cls, category_gateway: ICategoryRepository) -> 'UpdateCategoryUseCase':
        return cls(category_gateway)

    def execute(self, category_id: str, dto: UpdateCategoryDTO) -> Category:
        category = self.category_gateway.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        category.name = dto.name
        category.description = dto.description
        updated_category = self.category_gateway.update(category)

        return updated_category
