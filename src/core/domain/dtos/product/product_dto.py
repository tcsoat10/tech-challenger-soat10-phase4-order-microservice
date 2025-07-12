from pydantic import BaseModel

from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.entities.product import Product


class ProductDTO(BaseModel):
    id: int
    name: str
    description: str
    category: CategoryDTO
    price: float

    @classmethod
    def from_entity(cls, product: Product) -> "ProductDTO":
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            category=CategoryDTO.from_entity(product.category),
            price=product.price,
        )
