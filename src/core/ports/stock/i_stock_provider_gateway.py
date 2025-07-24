from typing import Dict, List, Any
from abc import ABC, abstractmethod


class IStockProviderGateway(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Retrieve a product by its ID."""
        pass

    @abstractmethod
    def get_products_by_category_name(self, category_id: str) -> List[Dict[str, Any]]:
        """Retrieve products by their category."""
        pass

    @abstractmethod
    def get_product_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve a product by its name."""
        pass

    @abstractmethod
    def get_categories(self) -> List[Dict[str, Any]]:
        """Retrieve all available categories."""
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: str) -> Dict[str, Any]:
        """Retrieve a category by its ID."""
        pass

    @abstractmethod
    def get_category_by_name(self, category_name: str) -> Dict[str, Any]:
        """Retrieve a category by its name."""
        pass
