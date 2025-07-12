from pydantic import BaseModel

from src.core.domain.entities.category import Category

class CategoryDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, category: Category) -> "CategoryDTO":
        return cls(id=category.id, name=category.name, description=category.description)