

import os
from unittest.mock import patch
from src.adapters.driven.providers.payment_provider.payment_provider_gateway import PaymentProviderGateway
from src.constants.payment_method_enum import PaymentMethodEnum
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO


@patch("requests.post")
def test_create_payment(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "payment_id": "123",
        "qr_code_link": "http://example.com/qr",
        "transaction_id": "abc"
    }

    gateway = PaymentProviderGateway()
    payment_data = CreatePaymentDTO(
        title="Test Payment",
        description="Payment for testing",
        payment_method=PaymentMethodEnum.QR_CODE.name,
        total_amount=100.0,
        currency="BRL",
        notification_url="http://example.com/callback",
        items=[],
        customer={}
    )

    result = gateway.create_payment(payment_data)

    assert result["payment_id"] == "123"
    assert result["qr_code"] == "http://example.com/qr"
    assert result["transaction_id"] == "abc"

@patch.dict(os.environ, {"PAYMENT_SERVICE_URL": "test-payment-provider.com"})
def test_read_base_url():
    gateway = PaymentProviderGateway()
    assert gateway.base_url == "http://test-payment-provider.com"

@patch.dict(os.environ, {"PAYMENT_SERVICE_URL": "test-payment-provider.com"})
def test_change_base_url():
    gateway = PaymentProviderGateway()
    new_url = "new-payment-provider.com"
    gateway.base_url = new_url
    assert gateway.base_url == f"http://{new_url}"
