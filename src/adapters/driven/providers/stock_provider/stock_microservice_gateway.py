from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException

import os
from typing import Dict, Any, List
from http import HTTPStatus
import requests


class StockMicroserviceGateway(IStockProviderGateway):
    """Gateway for interacting with the Stock Microservice."""
    
    def __init__(self):
        self._base_url = os.getenv("STOCK_MICROSERVICE_URL", "http://localhost:8003/api/v1")
        self._headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("STOCK_MICROSERVICE_X_API_KEY")
        }

    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Retrieve a product by its ID."""
        response = requests.get(f"{self._base_url}/products/{product_id}/id", headers=self._headers)
        
        if response.status_code != HTTPStatus.OK:
            raise EntityNotFoundException(message="Produto não encontrado", id=product_id)
        
        return response.json()
    
    def get_products_by_category_name(self, category_name: str) -> List[Dict[str, Any]]:
        """Retrieve products by their category."""
        response = requests.get(f"{self._base_url}/categories/{category_name}/products", headers=self._headers)
        
        if response.status_code == HTTPStatus.NOT_FOUND:
            return []
        response.raise_for_status()

        return response.json()

    def get_product_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve a product by its name."""
        # Assuming the endpoint returns a list and we want the first match.
        response = requests.get(f"{self._base_url}/products/{name}/name", headers=self._headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFoundException(message="Produto não encontrado", id=name)
        response.raise_for_status()

        results = response.json()
        if not results:
            raise EntityNotFoundException(message="Produto não encontrado", id=name)
        
        return results[0] # Returning the first result
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Retrieve all available categories."""
        response = requests.get(f"{self._base_url}/categories", headers=self._headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return []
        response.raise_for_status()

        return response.json()

    def get_category_by_id(self, category_id: str) -> Dict[str, Any]:
        """Retrieve a category by its ID."""
        response = requests.get(f"{self._base_url}/categories/{category_id}/id", headers=self._headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_id)
        response.raise_for_status()

        return response.json()

    def get_category_by_name(self, category_name: str) -> Dict[str, Any]:
        """Retrieve a category by its name."""
        response = requests.get(f"{self._base_url}/categories/{category_name}/name", headers=self._headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_name)
        response.raise_for_status()

        result = response.json()
        if not result:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_name)

        return result

