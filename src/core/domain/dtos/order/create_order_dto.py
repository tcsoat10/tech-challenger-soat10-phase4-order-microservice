from pydantic import BaseModel, ConfigDict

class CreateOrderDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

