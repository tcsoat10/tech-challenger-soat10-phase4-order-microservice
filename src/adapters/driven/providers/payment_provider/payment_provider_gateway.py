from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
import os
import requests


class PaymentProviderGateway(IPaymentProviderGateway):
    """
    Implementação do gateway de pagamento.
    """

    def __init__(self):
        self._base_url = os.getenv("PAYMENT_SERVICE_URL")
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("PAYMENT_SERVICE_API_KEY")
        }
    
    def create_payment(self, payment_data: CreatePaymentDTO) -> str:
        # Aqui você implementaria a lógica para criar um pagamento
        # utilizando o payment_data fornecido.
        # Por exemplo, enviar os dados para um serviço externo de pagamento.

        url = f"{self._base_url}/payment"
        response = requests.post(url, json=payment_data.dict(), headers=self._headers)
        response.raise_for_status()
        payment_id = response.json().get("payment_id")
        if not payment_id:
            raise ValueError("payment_id not found in payment service response")
        return payment_id