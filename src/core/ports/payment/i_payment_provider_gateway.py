
from typing import Dict, Any

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO

class IPaymentProviderGateway:
    """
    Interface para integração com o microsserviço de pagamento.
    """
    def create_payment(self, payment_data: CreatePaymentDTO) -> str:
        pass