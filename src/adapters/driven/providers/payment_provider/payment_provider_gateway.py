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
        """
        Creates a new payment by sending payment data to the external payment service.
        Args:
            payment_data (CreatePaymentDTO): The data required to create a payment.
        Returns:
            str: The unique identifier of the created payment.
        Raises:
            requests.HTTPError: If the HTTP request to the payment service fails.
            ValueError: If the response does not contain a 'payment_id'.
        """

        url = f"{self._base_url}/payment"
        response = requests.post(url, json=payment_data.model_dump(mode='json'), headers=self._headers)
        response.raise_for_status()
        payment_id = response.json().get("payment_id")
        if not payment_id:
            raise ValueError("payment_id not found in payment service response")
        return payment_id
