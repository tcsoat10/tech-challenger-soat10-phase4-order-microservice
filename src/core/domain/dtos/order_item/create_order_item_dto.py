from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CreateOrderItemDTO(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    order_id: Optional[int] = Field(None, gt=0)
    product_id: int = Field(..., gt=0)
    quantity: float = Field(..., ge=0.0)
    observation: str = Field(..., min_length=0, max_length=300)

