from pydantic import BaseModel, ConfigDict, Field

class CreateOrderStatusDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    status: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)

