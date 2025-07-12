from src.core.domain.entities.health_check import HealthCheck
from pydantic import BaseModel

class HealthCheckSchemaOut(BaseModel):
    status: str

    @classmethod
    def from_entity(cls, health_check: HealthCheck) -> "HealthCheckSchemaOut":
        return cls(status=health_check.status)
