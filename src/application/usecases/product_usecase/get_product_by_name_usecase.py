
from src.core.domain.entities.product import Product
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.product.i_product_repository import IProductRepository


class GetProductByNameUseCase:
    def __init__(self, product_gateway: IProductRepository):
        self.product_gateway = product_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository) -> 'GetProductByNameUseCase':
        return cls(product_gateway)

    def execute(self, name) -> Product:
        product = self.product_gateway.get_by_name(name=name)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        return product
