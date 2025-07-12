
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.product.i_product_repository import IProductRepository


class DeleteProductUseCase:
    def __init__(self, product_gateway: IProductRepository):
        self.product_gateway = product_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository) -> 'DeleteProductUseCase':
        return cls(product_gateway)
    
    def execute(self, product_id: int) -> None:
        product = self.product_gateway.get_by_id(product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")
        
        if DELETE_MODE == 'soft':
            if product.is_deleted():
                raise EntityNotFoundException(entity_name="Product")

            product.soft_delete()
            self.product_gateway.update(product)
        else:
            self.product_gateway.delete(product)
