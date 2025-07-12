from pydantic import BaseModel, ConfigDict, Field

class CreateProductDTO(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
    price: float = Field(..., ge=0.0)
    category_id: int = Field(..., gt=0)
