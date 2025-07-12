
from src.core.domain.entities.product import Product
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.product.i_product_repository import IProductRepository


class GetProductByIdUseCase:
    def __init__(self, product_gateway: IProductRepository):
        self.product_gateway = product_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository) -> 'GetProductByIdUseCase':
        return cls(product_gateway)
    
    def execute(self, product_id: int) -> Product:
        product = self.product_gateway.get_by_id(product_id=product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        return product
    
    