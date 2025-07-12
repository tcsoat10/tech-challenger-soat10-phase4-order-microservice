
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.entities.product import Product
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.ports.product.i_product_repository import IProductRepository


class UpdateProductUsecase:
    def __init__(self, product_gateway: IProductRepository, category_gateway: ICategoryRepository):
        self.product_gateway = product_gateway
        self.category_gateway = category_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository, category_gateway: ICategoryRepository) -> 'UpdateProductUsecase':
        return cls(product_gateway, category_gateway)
    
    def execute(self, product_id: int, dto: UpdateProductDTO) -> Product:
        product = self.product_gateway.get_by_id(product_id=product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        category = self.category_gateway.get_by_id(category_id=dto.category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        
        product.name = dto.name
        product.description = dto.description
        product.price = dto.price
        product.category = category
        self.product_gateway.update(product)
        
        return product
