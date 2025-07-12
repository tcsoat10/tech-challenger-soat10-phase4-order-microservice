
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.category.i_category_repository import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway = category_gateway
        
    @classmethod
    def build(cls, category_gateway: ICategoryRepository) -> 'DeleteCategoryUseCase':
        return cls(category_gateway)

    def execute(self, category_id: int) -> None:
        category = self.category_gateway.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        
        if DELETE_MODE == 'soft':
            if category.is_deleted():
                raise EntityNotFoundException(entity_name="Category")

            category.soft_delete()
            self.category_gateway.update(category)
        else:
            self.category_gateway.delete(category)
