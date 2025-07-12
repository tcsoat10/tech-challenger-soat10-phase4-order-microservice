from sqlalchemy import Column, String

from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.category import Category


class CategoryModel(BaseModel[Category]):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))
    
    @classmethod
    def from_entity(cls, entity: Category) -> "CategoryModel":
        return cls(
            id=getattr(entity, "id", None),
            created_at=getattr(entity, "created_at", None),
            updated_at=getattr(entity, "updated_at", None),
            inactivated_at=getattr(entity, "inactivated_at", None),
            name=entity.name,
            description=entity.description
        )
        
    def to_entity(self) -> Category:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Category, self.id)
        if existing:
            return existing
        
        category = Category(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            name=self.name,
            description=self.description
        )
        identity_map.add(category)
        return category



__all__ = ["CategoryModel"]
