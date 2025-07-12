from pydantic import BaseModel, ConfigDict, Field

class UpdateOrderDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    id_customer: int = Field(..., gt=0)
    id_order_status: int = Field(..., gt=0)
    id_employee: int = Field(..., gt=0)
