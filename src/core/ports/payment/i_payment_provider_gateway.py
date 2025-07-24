
from abc import ABC, abstractmethod
from typing import Dict, Any

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO

class IPaymentProviderGateway(ABC):
    """
    Interface para integração com o microsserviço de pagamento.
    """
    
    @abstractmethod
    def create_payment(self, payment_data: CreatePaymentDTO) -> str:
        """
        Cria um novo pagamento.
        Args:
            payment_data (CreatePaymentDTO): Dados necessários para criar o pagamento.
        Returns:
            str: ID do pagamento criado.
            str: qr_code do pagamento criado.
            str: transaction_id do pagamento criado.
        Raises:
            requests.HTTPError: Se a requisição HTTP falhar.
            ValueError: Se a resposta não contiver um 'payment_id'.
        """
        pass
    
    @abstractmethod
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Obtém os detalhes de um pagamento específico.
        
        Args:
            payment_id (str): O ID do pagamento a ser consultado.
        
        Returns:
            Dict[str, Any]: Detalhes do pagamento.
        """
        pass