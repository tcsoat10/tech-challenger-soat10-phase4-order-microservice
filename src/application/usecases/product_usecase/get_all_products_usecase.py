
from typing import List, Optional
from src.core.domain.entities.product import Product
from src.core.ports.product.i_product_repository import IProductRepository


class GetAllProductsUseCase:
    def __init__(self, product_gateway: IProductRepository):
        self.product_gateway = product_gateway
        
    @classmethod
    def build(cls, product_gateway: IProductRepository) -> 'GetAllProductsUseCase':
        return cls(product_gateway)
    
    def execute(self, categories: Optional[List[str]], include_deleted: Optional[bool] = False) -> List[Product]:
        products = self.product_gateway.get_all(categories, include_deleted)
        return products
