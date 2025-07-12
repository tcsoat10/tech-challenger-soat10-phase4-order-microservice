from src.schemas.health_check_schema import HealthCheckSchemaOut
from src.core.domain.entities.health_check import HealthCheck


class HealthCheckUseCase:
    def execute(self) -> HealthCheck:
        health_check = HealthCheck(status="healthy")
        return HealthCheckSchemaOut.from_entity(health_check)
