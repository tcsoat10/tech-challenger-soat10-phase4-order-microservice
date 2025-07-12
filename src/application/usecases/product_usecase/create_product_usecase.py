
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.entities.product import Product
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.ports.product.i_product_repository import IProductRepository


class CreateProductUsecase:
    def __init__(self, product_gateway: IProductRepository, category_gateway: ICategoryRepository):
        self.product_gateway = product_gateway
        self.category_gateway = category_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository, category_gateway: ICategoryRepository) -> 'CreateProductUsecase':
        return cls(product_gateway, category_gateway)

    def execute(self, dto: CreateProductDTO) -> Product:
        category = self.category_gateway.get_by_id(category_id=dto.category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        product = self.product_gateway.get_by_name(name=dto.name)
        if product:
            if not product.is_deleted():
                raise EntityDuplicatedException(entity_name="Product")
            
            product.name = dto.name
            product.description = dto.description
            product.price = dto.price
            product.category = category
            product.reactivate()
            self.product_gateway.update(product)
        else:
            product = Product(name=dto.name, description=dto.description, price=dto.price, category=category)
            product = self.product_gateway.create(product)

        return product
