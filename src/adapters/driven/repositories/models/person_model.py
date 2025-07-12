from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.person import Person
from sqlalchemy import Column, String, Date


class PersonModel(BaseModel):
    __tablename__ = "persons"

    name = Column(String(100))
    cpf = Column(String(11), unique=True)
    email = Column(String(150), unique=True)
    birth_date = Column(Date)
    
    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=getattr(entity, "id", None),
            created_at=getattr(entity, "created_at", None),
            updated_at=getattr(entity, "updated_at", None),
            inactivated_at=getattr(entity, "inactivated_at", None),
            name=entity.name,
            cpf=entity.cpf,
            email=entity.email,
            birth_date=entity.birth_date
        )
        
    def to_entity(self):
        identity_map = IdentityMap.get_instance()

        existing = identity_map.get(Person, self.id)
        if existing:
            return existing
        
        person = Person(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            name=self.name,
            cpf=self.cpf,
            email=self.email,
            birth_date=self.birth_date
        )
        identity_map.add(person)
        return person