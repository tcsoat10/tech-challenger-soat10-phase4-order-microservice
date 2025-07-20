from typing import TYPE_CHECKING, Optional
from src.core.domain.entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.core.domain.entities.order import Order
    from src.core.domain.entities.product import Product

class OrderItem(BaseEntity):
    
    def __init__(
        self,
        order: Optional['Order'] = None,
        quantity: Optional[int] = 1,
        observation: Optional[str] = "",
        product_price: Optional[float] = 0.0,
        product_name: Optional[str] = "",
        product_sku: Optional[str] = "",
        product_category_name: Optional[str] = "",
        product_id: Optional[str] = "",
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._order = order
        self._quantity = quantity
        self._observation = observation
        self._product_price = product_price
        self._product_name = product_name
        self._product_sku = product_sku
        self._product_category_name = product_category_name
        self._product_id = product_id


    @property
    def order(self) -> 'Order':
        return self._order

    @order.setter
    def order(self, value: 'Order'):
        self._order = value



    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        self._quantity = value

    @property
    def observation(self) -> Optional[str]:
        return self._observation

    @observation.setter
    def observation(self, value: Optional[str]):
        self._observation = value.strip() if value else value

    @property
    def product_price(self) -> float:
        return self._product_price
    
    @product_price.setter
    def product_price(self, value: float):
        if value < 0:
            raise ValueError("Product price cannot be negative")
        self._product_price = value

    @property
    def product_name(self) -> str:
        return self._product_name

    @product_name.setter
    def product_name(self, value: str):
        self._product_name = value.strip() if value else value

    @property
    def product_sku(self) -> str:
        return self._product_sku

    @product_sku.setter
    def product_sku(self, value: str):
        self._product_sku = value.strip() if value else value

    @property
    def product_category_name(self) -> str:
        return self._product_category_name

    @product_category_name.setter
    def product_category_name(self, value: str):
        self._product_category_name = value.strip() if value else value

    @property
    def product_id(self) -> str:
        return self._product_id

    @product_id.setter
    def product_id(self, value: str):
        if isinstance(value, str):
            self._product_id = value.strip()
        else:
            self._product_id = value

    @property
    def total(self) -> float:
        """
        Calculates the total cost of this item based on the product price and quantity.

        :return: Total cost as a float.
        """
        return self.product_price * self.quantity

    @property
    def product_category(self):
        """
        Retrieves the category of the associated product.

        :return: The category of the product.
        """
        return self.product_category_name
