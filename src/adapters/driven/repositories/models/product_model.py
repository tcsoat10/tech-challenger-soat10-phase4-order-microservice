from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.category_model import CategoryModel
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.product import Product
from src.core.shared.identity_map import IdentityMap

class ProductModel(BaseModel):
    __tablename__ = "products"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    category_id = Column(ForeignKey("categories.id"), nullable=False)
    category = relationship("CategoryModel")

    price = Column(Float, nullable=False, default=0.0)
    
    sla_product = Column(String(100), nullable=True)
    
    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=getattr(entity, "id", None),
            created_at=getattr(entity, "created_at", None),
            updated_at=getattr(entity, "updated_at", None),
            inactivated_at=getattr(entity, "inactivated_at", None),
            name=entity.name,
            description=entity.description,
            category_id=entity.category.id,
            price=entity.price,
            sla_product=entity.sla_product,
        )
        
    def to_entity(self):
        identity_map = IdentityMap.get_instance()
        
        existing = identity_map.get(Product, self.id)
        if existing:
            return existing

        product = Product(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            name=self.name,
            price=self.price,
            description=self.description,
            sla_product=self.sla_product,
        )
        identity_map.add(product)
        
        product.category = self.category.to_entity()
        
        return product
        

__all__ = ["ProductModel"]
