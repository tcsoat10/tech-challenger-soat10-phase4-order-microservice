from pydantic import BaseModel

class ProductDTO(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float

    @classmethod
    def from_dict(cls, product: dict) -> "ProductDTO":
        return cls(
            id=product.get("id"),
            name=product.get("name"),
            description=product.get("description"),
            category=product.get("category", {}).get("name") if product.get("category") else None,
            price=product.get("price")
        )
