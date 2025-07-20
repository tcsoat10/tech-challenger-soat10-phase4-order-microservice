from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO


class CreatePaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    title: str = Field(
        ...,
        description="Título do pagamento",
        example="Pagamento do pedido #12345",
    )
    description: str = Field(
        default="Pagamento do pedido",
        description="Descrição do pagamento",
        example="Pagamento do pedido #12345",
    )
    payment_method: str = Field(
        ...,
        description="Método de pagamento utilizado para o pagamento do pedido",
        example="qr_code",
    )
    total_amount: float = Field(
        ...,
        description="Valor total do pagamento",
        example=100.0,
    )
    currency: str = Field(
        ...,
        description="Moeda utilizada no pagamento",
        example="BRL",
    )
    notification_url: str = Field(
        ...,
        description="URL de callback para notificações de pagamento",
        example="https://example.com/callback",
    )
    items: list[OrderItemDTO] = Field(
        ...,
        description="Itens do pedido",
        example=[
            {
                "name": "item1",
                "description": "Item 1",
                "category": "hamburgers",
                "quantity": 1,
                "unit_price": 50.0
            },
            {
                "name": "item2",
                "description": "Item 2",
                "category": "drinks",
                "quantity": 1,
                "unit_price": 50.0
            }
        ]
    )
    customer: dict = Field(
        ...,
        description="Informações do cliente",
        example={
            "name": "João da Silva",
            "email": ""
        }
    )