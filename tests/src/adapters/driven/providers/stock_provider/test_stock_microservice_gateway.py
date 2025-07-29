import os
from unittest.mock import patch

from src.adapters.driven.providers.stock_provider.stock_microservice_gateway import StockMicroserviceGateway


@patch.dict(os.environ, {"STOCK_MICROSERVICE_URL": "test-stock-provider.com"})
def test_read_base_url():
    gateway = StockMicroserviceGateway()
    assert gateway.base_url == "http://test-stock-provider.com"

@patch.dict(os.environ, {"STOCK_MICROSERVICE_URL": "test-stock-provider.com"})
def test_change_base_url():
    gateway = StockMicroserviceGateway()
    new_url = "new-stock-provider.com"
    gateway.base_url = new_url
    assert gateway.base_url == f"http://{new_url}"

@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_product_by_id(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"id": "123", "name": "Test Product"}
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    product = gateway.get_product_by_id("123")

    assert product == {"id": "123", "name": "Test Product"}
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/products/123/id",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )


@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_products_by_category_name(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = [{"id": "123", "name": "Test Product"}]
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    products = gateway.get_products_by_category_name("Test Category")

    assert products == [{"id": "123", "name": "Test Product"}]
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/categories/Test Category/products",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )

@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_product_by_name(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = [{"id": "123", "name": "Test Product"}]
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    product = gateway.get_product_by_name("Test Product")

    assert product == {"id": "123", "name": "Test Product"}
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/products/Test Product/name",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )
    
@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_categories(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = [{"name": "Test Category"}]
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    categories = gateway.get_categories()

    assert categories == [{"name": "Test Category"}]
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/categories",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )

@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_category_by_id(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"id": "123", "name": "Test Category"}
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    category = gateway.get_category_by_id("123")

    assert category == {"id": "123", "name": "Test Category"}
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/categories/123/id",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )


@patch.dict(os.environ, {
    "STOCK_MICROSERVICE_URL": "test-stock-provider.com",
    "STOCK_MICROSERVICE_X_API_KEY": "test-api-key"
})
@patch("requests.get")
def test_get_category_by_name(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"id": "123", "name": "Test Category"}
    mock_response.status_code = 200

    gateway = StockMicroserviceGateway()
    category = gateway.get_category_by_name("Test Category")

    assert category == {"id": "123", "name": "Test Category"}
    mock_get.assert_called_once_with(
        "http://test-stock-provider.com/categories/Test Category/name",
        headers={
            'Content-Type': 'application/json',
            "x-api-key": "test-api-key"
        }
    )
