from pydantic import BaseModel, Field
from datetime import datetime


class PaymentWebhookDTO(BaseModel):
    event: str = Field(..., description="Tipo de evento do webhook, ex: 'payment.completed'")
    payment_id: str = Field(..., description="ID do pagamento no sistema de pagamentos")
    external_reference: str = Field(..., description="Referência externa do pagamento")
    amount: float = Field(..., description="Valor do pagamento")
    status: str = Field(..., description="Status do pagamento")
    transaction_id: str = Field(..., description="ID da transação no sistema de pagamentos")
    timestamp: datetime = Field(..., description="Data e hora do evento")

    class Config:
        json_schema_extra = {
            "example": {
                "event": "payment.completed",
                "payment_id": "123456789",
                "external_reference": "order_12345",
                "amount": 100.0,
                "status": "PAID",
                "transaction_id": "txn_987654321",
                "timestamp": "2023-10-01T12:00:00Z"
            }
        }

__all__ = ["PaymentWebhookDTO"]
