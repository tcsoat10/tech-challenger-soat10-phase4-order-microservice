from pydantic import BaseModel, ConfigDict, Field

class UpdateCategoryDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
