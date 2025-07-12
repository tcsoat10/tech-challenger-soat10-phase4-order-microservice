from enum import Enum


class PaymentMethodEnum(Enum):
    """
    Enumeração para os possíveis métodos de pagamento no sistema.
    """

    # CREDIT_CARD = ("credit_card", "Payment via credit card.")
    # DEBIT_CARD = ("debit_card", "Payment via debit card.")
    # PIX = ("pix", "Payment via PIX.")
    QR_CODE = ("qr_code", "Payment via QR Code.")

    @property
    def name(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def values_and_descriptions(cls):
        """
        Retorna todos os valores e descrições dos métodos de pagamento.
        :return: Lista de dicionários com o nome e descrição dos métodos.
        """
        return [{"name": member.name, "description": member.description} for member in cls]

    @classmethod
    def method_list(cls):
        """
        Retorna todos os nomes dos métodos de pagamento.
        :return: Lista de nomes dos métodos.
        """
        return [member.name for member in cls]

    @classmethod
    def to_dict(cls):
        """
        Retorna um dicionário mapeando os nomes dos métodos às suas descrições.
        :return: Dicionário com o nome como chave e a descrição como valor.
        """
        return {member.name: member.description for member in cls}
