from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.entities.order_status import OrderStatus

class OrderStatusDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    status: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)
    

    @classmethod
    def from_entity(cls, order_status: OrderStatus) -> "OrderStatusDTO":
        return cls(
            id=order_status.id,
            status=order_status.status,
            description=order_status.description
        )
    

    


