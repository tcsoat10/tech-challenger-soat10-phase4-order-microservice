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
            "x-api-key": os.getenv("STOCK_MICROSERVICE_API_KEY")
        }

    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Retrieve a product by its ID."""
        response = requests.get(f"{self._base_url}/products/{product_id}", headers=self._headers)
        
        if response.status_code != HTTPStatus.OK:
            raise EntityNotFoundException(message="Produto não encontrado", id=product_id)
        
        return response.json()
    
    def get_products_by_ids(self, product_ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieve multiple stock_microservice_gateway.pyproducts by their IDs."""
        response = requests.post(f"{self._base_url}/products/batch", json={"ids": product_ids}, headers=self._headers)
        
        if response.status_code != HTTPStatus.OK:
            raise EntityNotFoundException(message="Produtos não encontrados", entity="Products", ids=product_ids)
        
        return response.json()
    
    def get_products_by_category_id(self, category_id: str) -> List[Dict[str, Any]]:
        """Retrieve products by their category."""
        response = requests.get(f"{self._base_url}/categories/{category_id}/products", headers=self._headers)
        
        if response.status_code == HTTPStatus.NOT_FOUND:
            return []
        response.raise_for_status()

        return response.json()

    def get_product_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve a product by its name."""
        # Assuming the endpoint returns a list and we want the first match.
        response = requests.get(f"{self._base_url}/products", headers=self._headers, params={"name": name})

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
        response = requests.get(f"{self._base_url}/categories/{category_id}", headers=self._headers)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_id)
        response.raise_for_status()

        return response.json()

    def get_category_by_name(self, category_name: str) -> Dict[str, Any]:
        """Retrieve a category by its name."""
        response = requests.get(f"{self._base_url}/categories", headers=self._headers, params={"name": category_name})
        
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_name)
        response.raise_for_status()

        results = response.json()
        if not results:
            raise EntityNotFoundException(message="Categoria não encontrada", id=category_name)

        return results[0]

