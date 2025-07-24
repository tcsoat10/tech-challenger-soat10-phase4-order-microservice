
from pydantic import BaseModel, Field, ConfigDict


class PaymentDTO(BaseModel):
    """Data Transfer Object for Payment."""
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    payment_id: str = Field(..., min_length=1)
    qr_code: str = Field(..., min_length=1)
    transaction_id: str = Field(..., min_length=1)

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentDTO":
        return cls(
            payment_id=data.get("payment_id"),
            qr_code=data.get("qr_code"),
            transaction_id=data.get("transaction_id")
        )
