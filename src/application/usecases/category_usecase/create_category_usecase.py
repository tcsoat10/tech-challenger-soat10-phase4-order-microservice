from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.domain.entities.category import Category
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.category.i_category_repository import ICategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway = category_gateway
        
    @classmethod
    def build(cls, category_gateway: ICategoryRepository):
        return cls(category_gateway)

    def execute(self, dto: CreateCategoryDTO) -> Category:
        category = self.category_gateway.get_by_name(name=dto.name)
        if category:
            if not category.is_deleted():
                raise EntityDuplicatedException(entity_name="Category")
            
            category.name = dto.name
            category.description = dto.description
            category.reactivate()
            self.category_gateway.update(category)
        else:
            category = Category(name=dto.name, description=dto.description)
            category = self.category_gateway.create(category)

        return category