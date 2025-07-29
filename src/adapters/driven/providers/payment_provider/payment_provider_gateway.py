from typing import Any, Dict
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
import os
import requests


class PaymentProviderGateway(IPaymentProviderGateway):
    """
    Implementação do gateway de pagamento.
    """

    def __init__(self):
        self.base_url = os.getenv("PAYMENT_SERVICE_URL")
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("PAYMENT_SERVICE_API_KEY")
        }
        
    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, url: str):
        if not url.startswith('http'):
            url = f"http://{url}"
        self._base_url = url
    
    def create_payment(self, payment_data: CreatePaymentDTO) -> Dict[str, Any]:
        """
        Creates a new payment by sending payment data to the external payment service.
        Args:
            payment_data (CreatePaymentDTO): The data required to create a payment.
        Returns:
            str: ID do pagamento criado.
            str: qr_code do pagamento criado.
            str: transaction_id do pagamento criado.
        Raises:
            requests.HTTPError: If the HTTP request to the payment service fails.
            ValueError: If the response does not contain a 'payment_id'.
        """

        response = requests.post(
            f"{self.base_url}/payment",
            headers=self._headers,
            json=payment_data.model_dump(mode='json'),
        )
        response.raise_for_status()
        
        response = response.json()
        if not response:
            raise ValueError("payment_id not found in payment service response")

        return {
            "payment_id": response.get("payment_id"),
            "qr_code": response.get("qr_code_link"),
            "transaction_id": response.get("transaction_id"),
        }

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Retrieves the details of a specific payment by its ID.
        
        Args:
            payment_id (str): The ID of the payment to retrieve.
        
        Returns:
            Dict[str, Any]: The details of the payment.
        
        Raises:
            requests.HTTPError: If the HTTP request to the payment service fails.
            ValueError: If the response does not contain payment details.
        """
        response = requests.get(f"{self.base_url}/payment/id/{payment_id}", headers=self._headers)
        response.raise_for_status()
        
        payment_details = response.json()
        if not payment_details:
            raise ValueError("Payment details not found")
        
        return payment_details
