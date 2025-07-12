
from typing import Optional
from src.application.usecases.category_usecase.get_all_categories_usecase import GetAllCategoriesUseCase
from src.application.usecases.category_usecase.get_category_by_id_usecase import GetCategoryByIdUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.category_usecase.get_category_by_name_usecase import GetCategoryByNameUseCase
from src.application.usecases.category_usecase.create_category_usecase import CreateCategoryUseCase
from src.application.usecases.category_usecase.update_category_usecase import UpdateCategoryUseCase
from src.application.usecases.category_usecase.delete_category_usecase import DeleteCategoryUseCase
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.ports.category.i_category_repository import ICategoryRepository

class CategoryController:
    def __init__(self, category_gateway: ICategoryRepository):
        self.category_gateway: ICategoryRepository = category_gateway

    def create_category(self, dto: CreateCategoryDTO) -> CategoryDTO:
        create_category_usecase = CreateCategoryUseCase.build(self.category_gateway)
        category = create_category_usecase.execute(dto)
        return DTOPresenter.transform(category, CategoryDTO)

    def get_category_by_name(self, name: str) -> CategoryDTO:
        category_by_name_usecase = GetCategoryByNameUseCase.build(self.category_gateway)
        category = category_by_name_usecase.execute(name)
        return DTOPresenter.transform(category, CategoryDTO)

    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        category_by_id_usecase = GetCategoryByIdUseCase.build(self.category_gateway)
        category = category_by_id_usecase.execute(category_id)
        return DTOPresenter.transform(category, CategoryDTO)

    def get_all_categories(self, include_deleted: Optional[bool] = False) -> list[CategoryDTO]:
        all_categories_usecase = GetAllCategoriesUseCase.build(self.category_gateway)
        categories = all_categories_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(categories, CategoryDTO)

    def update_category(self, category_id: int, dto: CreateCategoryDTO) -> CategoryDTO:
        update_category_usecase = UpdateCategoryUseCase.build(self.category_gateway)
        category = update_category_usecase.execute(category_id, dto)
        return DTOPresenter.transform(category, CategoryDTO)

    def delete_category(self, category_id: int) -> None:
        delete_category_usecase = DeleteCategoryUseCase.build(self.category_gateway)
        delete_category_usecase.execute(category_id)
