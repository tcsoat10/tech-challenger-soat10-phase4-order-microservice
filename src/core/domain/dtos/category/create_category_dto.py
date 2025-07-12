from pydantic import BaseModel, ConfigDict, Field

class CreateCategoryDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=300)
