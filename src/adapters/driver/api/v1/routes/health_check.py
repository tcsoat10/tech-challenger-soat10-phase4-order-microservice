from src.schemas.health_check_schema import HealthCheckSchemaOut
from src.application.usecases.health_check_usecase.health_check_usecase import HealthCheckUseCase
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", response_model=HealthCheckSchemaOut, status_code=status.HTTP_200_OK)
async def health_check():
    return HealthCheckUseCase().execute()
